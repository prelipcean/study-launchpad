#!/usr/bin/env bash
# Bootstrap a new book-study project from this toolkit.
set -euo pipefail

TOOLKIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    cat <<'EOF'
Bootstrap a new book-study project from this toolkit.

  ./init.sh <target-dir> [path/to/book.pdf]

Copies .claude/ and scripts/ into the target directory (creating it if
needed), copies a PDF in if you name one, and leaves the rest to /plan-book.
Never overwrites anything already there — re-running on a live project is a
safe no-op you can use to check nothing's missing.
EOF
}

if [ $# -lt 1 ]; then
    usage
    exit 1
fi

TARGET="$1"
PDF="${2:-}"

if [ -n "$PDF" ] && [ ! -f "$PDF" ]; then
    echo "error: no such PDF: $PDF" >&2
    exit 1
fi

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

if [ "$TARGET" = "$TOOLKIT" ]; then
    echo "error: target is the toolkit directory itself." >&2
    echo "Pick a separate directory for the book project." >&2
    exit 1
fi

for dir in .claude scripts; do
    if [ -e "$TARGET/$dir" ]; then
        echo "skip  $dir/ (already exists)"
    else
        cp -r "$TOOLKIT/$dir" "$TARGET/$dir"
        echo "copy  $dir/"
    fi
done

# Personal permission grants accumulated while working on the toolkit itself.
# They are not part of it, and don't belong in a fresh project.
rm -f "$TARGET/.claude/settings.local.json"

if [ -n "$PDF" ]; then
    base="$(basename "$PDF")"
    if [ -e "$TARGET/$base" ]; then
        echo "skip  $base (already exists)"
    else
        cp "$PDF" "$TARGET/$base"
        echo "copy  $base"
    fi
fi

pdf_count=$(find "$TARGET" -maxdepth 1 -name '*.pdf' | wc -l | tr -d ' ')

echo
echo "Project ready at $TARGET"
if [ "$pdf_count" -eq 0 ]; then
    echo "Next: copy the book PDF in, then run 'claude' there and /plan-book"
else
    if [ "$pdf_count" -gt 1 ]; then
        echo "Note: $pdf_count PDFs present — /plan-book will ask which one to use."
    fi
    echo "Next: run 'claude' there and /plan-book"
fi
