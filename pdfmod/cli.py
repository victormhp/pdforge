import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

import pdfmod.cat
import pdfmod.meta
import pdfmod.rm
import pdfmod.rotate
import pdfmod.secure


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pdfmod",
        description="pdfmod: iLovePDF made in home.",
        epilog="For help with a specific command, see: `pdfmod <command> -h`.",
    )

    ps_commands = parser.add_subparsers(title="commands", help="PDF Utilities", dest="command")

    # ---------------------------------------------------------------------------------------------
    # 'cat' command
    # ---------------------------------------------------------------------------------------------
    ps_cat = ps_commands.add_parser(
        "cat", help="Merge multiple PDF files into a single PDF document"
    )
    ps_cat.add_argument(
        "input",
        nargs="+",
        help="Path to the input PDF files to merge. Optionally specify a page or page range in the format 'file.pdf:page' or 'file.pdf:start-end'",
        metavar="FILE[:PAGES]]",
    )
    ps_cat.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="output filename",
        metavar="OUTPUT",
    )
    ps_cat.set_defaults(func=pdfmod.cat.main)

    # ---------------------------------------------------------------------------------------------
    # 'rm' command
    # ---------------------------------------------------------------------------------------------
    ps_rm = ps_commands.add_parser(
        "rm",
        help="Remove specified pages from a PDF and create a new file with the remaining pages",
    )
    ps_rm.add_argument("input", type=Path, help="Path to the input PDF file.", metavar="INPUT")
    ps_rm.add_argument(
        "pages",
        help="Pages to remove from the PDF file. Specify as single values (e.g., 3), ranges (e.g., 2-5), or a comma-separated list (e.g., 1,3,6-8)",
        metavar="PAGES",
    )
    ps_rm.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="output filename",
        metavar="OUTPUT",
    )
    ps_rm.set_defaults(func=pdfmod.rm.main)

    # ---------------------------------------------------------------------------------------------
    # 'secure' command
    # ---------------------------------------------------------------------------------------------
    ps_secure = ps_commands.add_parser("secure", help="Encrypt or decrypt a PDF file")

    ps_secure.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_secure.add_argument(
        "password", help="Password to encrypt or decrypt the PDF file", metavar="PASSWORD"
    )
    ps_secure.add_argument(
        "-m",
        "--mode",
        choices=["encrypt", "decrypt"],
        required=True,
        help="Choose whether to encrypt or decrypt the PDF file",
        metavar="MODE",
    )
    ps_secure.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        help="Output filename for the processed PDF file. If not provided, it will be named 'filename'-'mode'.pdf",
        metavar="OUTPUT",
    )
    ps_secure.set_defaults(func=pdfmod.secure.main)

    # ---------------------------------------------------------------------------------------------
    # 'meta' command
    # ---------------------------------------------------------------------------------------------
    ps_meta = ps_commands.add_parser("meta", help="Retrieve metadata from a PDF file")

    ps_meta.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_meta.set_defaults(func=pdfmod.meta.main)

    # ---------------------------------------------------------------------------------------------
    # 'rotate' command
    # ---------------------------------------------------------------------------------------------
    ps_rotate = ps_commands.add_parser(
        "rotate",
        help="Rotate page horizontally or vertically",
    )
    ps_rotate.add_argument("input", type=Path, help="Path to the input PDF file.", metavar="INPUT")
    ps_rotate.add_argument(
        "pages",
        help="Pages to rotate",
        metavar="PAGES",
    )
    ps_rotate.add_argument(
        "-r",
        "--rotation",
        default="left",
        choices=pdfmod.rotate.rotations_map.keys(),
        help="Rotation direction. Choose from: left, right, upside-down. Defaults to left",
        metavar="ROTATION",
    )
    ps_rotate.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="output filename",
        metavar="OUTPUT",
    )
    ps_rotate.set_defaults(func=pdfmod.rotate.main)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    else:
        args.func(args)
        sys.exit(0)
