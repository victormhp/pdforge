from pathlib import Path
from typing import Optional, Sequence

import pymupdf
import pytest

import pdfmod.cli


def run_cli(args: Optional[Sequence[str]] = None):
    try:
        pdfmod.cli.main(args)
    except SystemExit as error:
        return error.code


@pytest.fixture()
def sample_pdf(tmp_path: Path):
    doc = pymupdf.open()
    for i in range(10):
        page = doc.new_page()
        page.insert_text((50, 50), f"Sample PDF for Testing - Page {i + 1}", fontsize=24)

    output = tmp_path / "sample.pdf"
    doc.save(output)
    doc.close()
    return output


@pytest.fixture()
def encrypted_pdf(tmp_path: Path):
    doc = pymupdf.open()
    for i in range(10):
        page = doc.new_page()
        page.insert_text((50, 50), f"Encrypted PDF for Testing - Page {i + 1}", fontsize=24)

    output = tmp_path / "encrypted.pdf"
    doc.save(output, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="pepelotas")
    doc.close()
    return output
