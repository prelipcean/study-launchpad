#!/usr/bin/env python3
"""Fallback OCR for a single PDF page, for when Claude's rendered view of the
page isn't legible (dense diagram, scanned text, etc). Normal chapter reading
should go through the Read tool directly, not this script.

Usage: python3 ocr_page.py <page_number> [pdf_path]
Page numbers are 1-indexed, matching the Read tool's `pages` convention.
If pdf_path is omitted, the single PDF file in the current directory is
used.
"""
import glob
import sys

import fitz  # pymupdf
import pytesseract
from PIL import Image

DPI = 300


def find_default_pdf():
    pdfs = glob.glob("*.pdf")
    if len(pdfs) != 1:
        sys.exit(
            f"Expected exactly one PDF in the current directory, found {len(pdfs)}. "
            "Pass the path explicitly: python3 ocr_page.py <page_number> <pdf_path>"
        )
    return pdfs[0]


def render(pdf_path, page_num):
    """Rasterize one 1-indexed page to a PIL image."""
    with fitz.open(pdf_path) as doc:
        if not 1 <= page_num <= doc.page_count:
            sys.exit(
                f"Page {page_num} is out of range: {pdf_path} has "
                f"{doc.page_count} pages (1-{doc.page_count})."
            )
        pixmap = doc[page_num - 1].get_pixmap(dpi=DPI)
    return Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    try:
        page_num = int(sys.argv[1])
    except ValueError:
        sys.exit(f"Page number must be an integer, got {sys.argv[1]!r}.")

    pdf_path = sys.argv[2] if len(sys.argv) > 2 else find_default_pdf()
    print(pytesseract.image_to_string(render(pdf_path, page_num)))


if __name__ == "__main__":
    main()
