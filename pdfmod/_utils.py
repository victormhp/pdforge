import re
import sys
from pathlib import Path
from typing import Tuple

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
    except Exception as e:
        error_args(e)


def parse_pages_range(doc: pymupdf.Document, pages: str) -> Tuple[int, int]:
    if not re.match(r"^\d+-\d+$", pages):
        error_args(f"Invalid page range. '{pages}' must be 'start-end' with positive integers")

    num_pages = doc.page_count
    start, end = map(int, pages.split("-"))
    if start < 1 or end < 1 or start >= num_pages or end > num_pages or start > end:
        error_args(f"Invalid page range. {start}-{end} out of bounds")

    return start, end
