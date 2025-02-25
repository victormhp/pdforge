from dataclasses import dataclass
from pathlib import Path

import pymupdf

from pdfmod._utils import open_pdf, parse_pages_range


@dataclass
class PdfJoinArgs:
    input: list[str]
    output: str


def main(args: PdfJoinArgs) -> None:
    files = args.input
    doc = pymupdf.open()
    for f in files:
        opts = f.split(":", 2)
        path = opts[0]
        password = opts[2] if len(opts) > 2 else ""

        src = open_pdf(Path(path), password)

        pages = opts[1] if len(opts) > 1 else ""
        start, end = 1, src.page_count
        if pages:
            start, end = parse_pages_range(src, pages)

        doc.insert_pdf(src, from_page=start - 1, to_page=end - 1)
        src.close()

    doc.save(args.output, garbage=4, deflate=True)
    doc.close()
    print(f"Merged PDF files into {args.output}")
