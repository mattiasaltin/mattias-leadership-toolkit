#!/usr/bin/env bash
# Create docs/ symlink layer for MkDocs (content stays at repo root).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="$ROOT/docs"

rm -rf "$DOCS"
mkdir -p "$DOCS"

ln -s ../README.md "$DOCS/README.md"
ln -s ../CONTRIBUTING.md "$DOCS/CONTRIBUTING.md"
ln -s ../CODE_OF_CONDUCT.md "$DOCS/CODE_OF_CONDUCT.md"
ln -s ../LICENSE "$DOCS/LICENSE"
ln -s ../engineering-leadership-resources "$DOCS/engineering-leadership-resources"
ln -s ../product-leadership-resources "$DOCS/product-leadership-resources"
