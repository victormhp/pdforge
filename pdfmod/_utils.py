import re
import sys
from pathlib import Path
from typing import Set

import pymupdf


def error_args(msg: str, code=2) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def open_pdf(path: Path, password="") -> pymupdf.Document:
    try:
        doc = pymupdf.open(path)

        if not doc.is_pdf:
            error_args(f"{path}'not a pdf")
        if not doc.needs_pass:
            return doc

        if password:
            rc = doc.authenticate(password)
            if not rc:
                error_args(f"'{path.name}' authentication failed")
            return doc
        else:
            error_args(f"'{path.name}' requires a password")
    except pymupdf.FileNotFoundError as e:
        error_args(e)
    except pymupdf.FileDataError as e:
        error_args(e)
    except Exception as e:
        error_args(e)


def parse_pages(doc: pymupdf.Document, pages: str) -> Set[int]:
    nums = set()
    pages_arr = pages.split(",")

    for p in pages_arr:
        p = p.strip()

        if re.match(r"^\d+$", p):
            is_valid_page(doc, int(p))
            nums.add(int(p) - 1)
        elif re.match(r"^\d+-\d+$", p):
            start, end = map(int, p.split("-", 1))
            is_valid_page_range(doc, start, end)
            nums.update(range(start - 1, end))
        else:
            error_args(f"Invalid page range: {pages}")

    return nums


def is_valid_page(doc: pymupdf.Document, page: int) -> None:
    page_count = doc.page_count
    if page < 1 or page > page_count:
        error_args(f"Invalid page range: {page}. Must be within 1 and {page_count}")


def is_valid_page_range(doc: pymupdf.Document, start: int, end: int) -> None:
    page_count = doc.page_count
    if start < 1 or end < 1 or start > page_count or end > page_count or start > end:
        error_args(f"Invalid page range: {start}-{end}. Must be within 1 and {page_count}")
