#!/usr/bin/env python3
"""Assert topic pages appear in indexes, prev/next chains, and mkdocs.yml nav.

Exit code 0 = OK, 1 = navigation drift found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_NAMES = {
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CLAUDE.md",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PREV_RE = re.compile(r"\[⬅️ Previous:[^\]]*\]\(([^)]+)\)")
NEXT_RE = re.compile(r"\[➡️ Next:[^\]]*\]\(([^)]+)\)")
# Paths listed in mkdocs.yml nav (markdown files under docs/)
MKDOCS_PATH_RE = re.compile(
    r"(?:^|\n)\s*-\s+[^:]+:\s+"
    r"((?:engineering|product)-leadership-resources/[^\s]+\.md|README\.md)"
)


def topic_files(directory: Path) -> list[Path]:
    return sorted(
        p
        for p in directory.glob("*.md")
        if p.name not in SKIP_NAMES and p.is_file()
    )


def linked_basenames(markdown: str) -> set[str]:
    names: set[str] = set()
    for target in LINK_RE.findall(markdown):
        target = target.split()[0].strip("<>")
        file_part = target.split("#", 1)[0]
        if file_part.endswith(".md"):
            names.add(Path(file_part).name)
    return names


def check_indexed(topics: list[Path], index: Path, errors: list[str]) -> None:
    if not index.exists():
        errors.append(f"Missing index: {index.relative_to(ROOT)}")
        return
    indexed = linked_basenames(index.read_text(encoding="utf-8"))
    for topic in topics:
        if topic.name not in indexed:
            errors.append(
                f"{topic.relative_to(ROOT)} missing from {index.relative_to(ROOT)}"
            )


def check_chain(topics: list[Path], errors: list[str]) -> None:
    """Verify prev/next form a single chain covering all topics in browse order."""
    by_name = {t.name: t for t in topics}
    starts: list[Path] = []
    for topic in topics:
        text = topic.read_text(encoding="utf-8")
        prev = PREV_RE.search(text)
        nxt = NEXT_RE.search(text)
        if prev:
            prev_name = Path(prev.group(1).split()[0]).name
            if prev_name not in by_name:
                errors.append(
                    f"{topic.relative_to(ROOT)} previous points to unknown {prev_name}"
                )
            else:
                prev_text = by_name[prev_name].read_text(encoding="utf-8")
                prev_next = NEXT_RE.search(prev_text)
                if not prev_next or Path(prev_next.group(1).split()[0]).name != topic.name:
                    errors.append(
                        f"{topic.relative_to(ROOT)} previous {prev_name} does not next back"
                    )
        else:
            starts.append(topic)
        if nxt:
            next_name = Path(nxt.group(1).split()[0]).name
            if next_name not in by_name:
                errors.append(
                    f"{topic.relative_to(ROOT)} next points to unknown {next_name}"
                )

    if len(starts) != 1:
        names = ", ".join(p.name for p in starts) or "(none)"
        errors.append(
            f"{topics[0].parent.relative_to(ROOT)}: expected exactly one chain start, "
            f"found {len(starts)}: {names}"
        )
        return

    visited: list[str] = []
    current = starts[0]
    while current is not None:
        if current.name in visited:
            errors.append(
                f"{topics[0].parent.relative_to(ROOT)}: cycle at {current.name}"
            )
            return
        visited.append(current.name)
        text = current.read_text(encoding="utf-8")
        nxt = NEXT_RE.search(text)
        if not nxt:
            current = None
        else:
            current = by_name.get(Path(nxt.group(1).split()[0]).name)

    missing = sorted(by_name.keys() - set(visited))
    if missing:
        errors.append(
            f"{topics[0].parent.relative_to(ROOT)}: topics not in prev/next chain: "
            + ", ".join(missing)
        )


def check_mkdocs_nav(topic_paths: list[Path], errors: list[str]) -> None:
    mkdocs = ROOT / "mkdocs.yml"
    if not mkdocs.exists():
        errors.append("Missing mkdocs.yml")
        return
    text = mkdocs.read_text(encoding="utf-8")
    listed = set(MKDOCS_PATH_RE.findall(text))
    for topic in topic_paths:
        rel = topic.relative_to(ROOT).as_posix()
        if rel not in listed:
            errors.append(f"{rel} missing from mkdocs.yml nav")


def main() -> int:
    errors: list[str] = []
    all_topics: list[Path] = []

    eng_root = ROOT / "engineering-leadership-resources"
    eng_readme = eng_root / "README.md"
    for section in ("org-health", "tech-health", "delivery-execution"):
        section_dir = eng_root / section
        topics = topic_files(section_dir)
        all_topics.extend(topics)
        check_indexed(topics, section_dir / "README.md", errors)
        check_indexed(topics, eng_readme, errors)
        check_chain(topics, errors)

    # other/ is an author-notes shelf (README only today). If topic files appear, require index.
    other_dir = eng_root / "other"
    other_topics = topic_files(other_dir)
    if other_topics:
        check_indexed(other_topics, other_dir / "README.md", errors)
        check_indexed(other_topics, eng_readme, errors)
        all_topics.extend(other_topics)

    product_root = ROOT / "product-leadership-resources"
    product_topics = topic_files(product_root)
    all_topics.extend(product_topics)
    check_indexed(product_topics, product_root / "README.md", errors)
    check_chain(product_topics, errors)

    check_mkdocs_nav(all_topics, errors)

    if errors:
        print("Navigation check failed:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Navigation check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
