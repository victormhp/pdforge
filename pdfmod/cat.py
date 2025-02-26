from dataclasses import dataclass
from pathlib import Path

import pymupdf

from pdfmod._utils import open_pdf, parse_pages


@dataclass
class PdfCatArgs:
    input: list[str]
    output = "output.pdf"


def main(args: PdfCatArgs) -> None:
    files = args.input
    output = args.output or "output.pdf"

    doc = pymupdf.open()
    for f in files:
        opts = f.split(":", 2)
        path = Path(opts[0])
        password = opts[2] if len(opts) > 2 else ""

        src = open_pdf(path, password)

        pages = opts[1] if len(opts) > 1 else ""
        start, end = 0, src.page_count - 1
        if pages:
            pages_parsed = parse_pages(src, pages)
            start, end = min(pages_parsed), max(pages_parsed)

        doc.insert_pdf(src, from_page=start, to_page=end)
        src.close()

    doc.save(output, garbage=4, deflate=True)
    doc.close()
    print(f"Merged PDF files into {output}")
