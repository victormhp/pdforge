from pathlib import Path

import pytest

from .conftest import run_cli


@pytest.mark.parametrize("opts", [":", ":1", ":1-5"])
def test_cat(sample_pdf: Path, capsys: pytest.CaptureFixture, opts: str):
    output_pdf = str(sample_pdf.parent / "output.pdf")
    input_pdf = str(sample_pdf) + opts

    error_code = run_cli(["cat", input_pdf, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert err == ""
    assert "Merged PDF files" in out


@pytest.mark.parametrize("page_range", ["a", "-", "1-", "0-1", "1-1000", "1000-1", "1-1-1"])
def test_cat_invalid_range(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = f"{sample_pdf}:{page_range}"
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["cat", input_pdf, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert out == ""
    assert "Invalid page range" in err
