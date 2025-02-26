from dataclasses import dataclass
from pathlib import Path

from pdfmod._utils import open_pdf, parse_pages


@dataclass
class PdfRemoveArgs:
    path: str
    pages: str
    output: str


def main(args: PdfRemoveArgs) -> None:
    path = Path(args.path)
    pages = args.pages
    output = args.output

    src = open_pdf(path)
    pages_parsed = parse_pages(src, pages)

    src.delete_pages(list(pages_parsed))
    src.save(output, garbage=4, deflate=True)

    src.close()
    print(f"Removed pages and saved to '{output}'")
