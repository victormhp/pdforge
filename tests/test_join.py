from pathlib import Path

import pytest

from .conftest import run_cli


@pytest.mark.parametrize("opts", [":", "::", ":1-5", ":1-5:password"])
def test_join(sample_pdf: Path, capsys: pytest.CaptureFixture, opts: str):
    output_pdf = str(sample_pdf.parent / "output.pdf")
    input_pdf = str(sample_pdf) + opts

    error_code = run_cli(["join", input_pdf, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert err == ""
    assert "Merged PDF files" in out


@pytest.mark.parametrize("page_range", ["a", "-", "1-", "0-1", "1-1000", "1000-1", "1-1-1"])
def test_join_invalid_range(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = f"{sample_pdf}:{page_range}"
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["join", input_pdf, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert out == ""
    assert "Invalid page range" in err


def test_join_encrypted(encrypted_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = f"{encrypted_pdf}::pepelotas"
    output_pdf = str(encrypted_pdf.parent / "output.pdf")

    error_code = run_cli(["join", input_pdf, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert err == ""
    assert "Merged PDF files" in out


def test_join_encrypted_failed(encrypted_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = f"{encrypted_pdf}::bad_password"
    output_pdf = str(encrypted_pdf.parent / "output.pdf")

    error_code = run_cli(["join", input_pdf, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert out == ""
    assert "authentication failed" in err
