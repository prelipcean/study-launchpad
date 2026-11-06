#!/usr/bin/env python3
"""Print a PDF's total page count — used by plan-book to bound the last
chapter's range and locate the back matter.

Usage: python3 page_count.py [pdf_path]
If pdf_path is omitted, the single PDF file in the current directory is used.
"""
import glob
import sys

import fitz  # pymupdf


def find_default_pdf():
    pdfs = glob.glob("*.pdf")
    if len(pdfs) != 1:
        sys.exit(
            f"Expected exactly one PDF in the current directory, found {len(pdfs)}. "
            "Pass the path explicitly: python3 page_count.py <pdf_path>"
        )
    return pdfs[0]


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else find_default_pdf()
    with fitz.open(pdf_path) as doc:
        print(doc.page_count)


if __name__ == "__main__":
    main()
