#!/usr/bin/env python3
"""Detect soft-404s on curated citation hosts (HTTP 200 but wrong page).

Checks:
  - YouTube / youtu.be → oEmbed must succeed
  - Watched hosts → title must not look like a 404 page
  - Watched hosts → a deep path must not land on the site homepage

Exit 0 = OK, 1 = problems found.
"""

from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_PARTS = {
    "node_modules",
    ".venv",
    "venv",
    "tmp",
    "docs",
    "site",
    ".git",
}

# Hosts (suffix match) that historically soft-404 while returning HTTP 200.
WATCH_HOSTS = (
    "svpg.com",
    "thoughtworks.com",
    "rework.withgoogle.com",
    "sei.cmu.edu",
    "producttalk.org",
    "jpattonassociates.com",
    "intercom.com",
    "productplan.com",
    "ncsc.gov.uk",
    "owasp.org",
    "martinfowler.com",
    "dora.dev",
    "c4model.com",
    "teamtopologies.com",
    "lean.org",
    "agilemanifesto.org",
    "scrumguides.org",
    "whatmatters.com",
    "basecamp.com",
    "sre.google",
    "aws.amazon.com",
    "landscape.cncf.io",
    "aboutamazon.com",
    "gov.uk",
    "gayle.com",
    "larahogan.me",
    "hbr.org",
    "microsoft.com",
    "github.blog",
)

LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
BAD_TITLE_RE = re.compile(
    r"\b404\b|page not found|not found|access denied|attention required",
    re.I,
)
YOUTUBE_RE = re.compile(
    r"(?:youtube\.com/watch\?|youtu\.be/|youtube\.com/embed/)",
    re.I,
)

UA = (
    "Mozilla/5.0 (compatible; mattias-leadership-toolkit-citation-check/1.0; "
    "+https://github.com/mattiasaltin/mattias-leadership-toolkit)"
)


def md_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIR_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def host_watched(host: str) -> bool:
    host = host.lower().removeprefix("www.")
    return any(host == h or host.endswith("." + h) for h in WATCH_HOSTS)


def youtube_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if "youtu.be" in host:
        vid = parsed.path.strip("/").split("/")[0]
        return vid or None
    if "youtube.com" in host:
        if parsed.path.startswith("/watch"):
            return parse_qs(parsed.query).get("v", [None])[0]
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"}:
            return parts[1]
    return None


def fetch(url: str, timeout: float = 20.0) -> tuple[int, str, str]:
    """Return status, final_url, body (or empty)."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "text/html,application/json,*/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(200_000).decode("utf-8", errors="replace")
            return resp.getcode() or 0, resp.geturl(), body
    except urllib.error.HTTPError as exc:
        body = exc.read(200_000).decode("utf-8", errors="replace") if exc.fp else ""
        return exc.code, exc.geturl() if hasattr(exc, "geturl") else url, body
    except Exception as exc:  # noqa: BLE001 - surface as soft failure
        return 0, url, str(exc)


def page_title(body: str) -> str:
    match = TITLE_RE.search(body)
    if not match:
        return ""
    title = unescape(re.sub(r"\s+", " ", match.group(1)).strip())
    return title


def is_homepage(final_url: str) -> bool:
    parsed = urlparse(final_url)
    path = parsed.path.rstrip("/") or "/"
    return path == "/" and not parsed.query


def had_deep_path(url: str) -> bool:
    path = urlparse(url).path.rstrip("/")
    return bool(path) and path != "/"


def check_youtube(url: str, errors: list[str], cache: dict[str, str | None]) -> None:
    vid = youtube_id(url)
    if not vid:
        errors.append(f"unrecognised YouTube URL: {url}")
        return
    if vid in cache:
        title = cache[vid]
    else:
        oembed = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        status, _, body = fetch(oembed)
        time.sleep(0.15)
        title = body if status == 200 else None
        cache[vid] = title
    if not title:
        errors.append(f"YouTube unavailable (oEmbed failed): {url}")


def check_watched(url: str, errors: list[str], cache: dict[str, tuple[int, str, str]]) -> None:
    if url in cache:
        status, final, body = cache[url]
    else:
        status, final, body = fetch(url)
        time.sleep(0.2)
        cache[url] = (status, final, body)

    if status == 0:
        errors.append(f"fetch failed: {url} ({body[:120]})")
        return
    if status >= 400:
        errors.append(f"HTTP {status}: {url} → {final}")
        return

    title = page_title(body)
    if title and BAD_TITLE_RE.search(title):
        errors.append(f"bad title {title!r}: {url} → {final}")
        return

    if had_deep_path(url) and is_homepage(final):
        errors.append(f"soft-404 to homepage: {url} → {final} (title={title!r})")


def main() -> int:
    errors: list[str] = []
    yt_cache: dict[str, str | None] = {}
    page_cache: dict[str, tuple[int, str, str]] = {}
    checked = 0

    for path in md_files():
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            url = raw.strip().rstrip(").,;")
            host = urlparse(url).netloc.lower()
            if YOUTUBE_RE.search(url):
                check_youtube(url, errors, yt_cache)
                checked += 1
            elif host_watched(host):
                check_watched(url, errors, page_cache)
                checked += 1

    if errors:
        print(f"Citation check failed ({len(errors)} issue(s), {checked} URLs checked):\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Citation check passed ({checked} watched URLs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
