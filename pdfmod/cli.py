import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

import pdfmod.cat
import pdfmod.rm


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
    ps_rm.add_argument(
        "input",
        type=Path,
        help="Path to the input PDF file.",
        metavar="INPUT",
    )
    ps_rm.add_argument(
        "pages",
        help="Pages to remove from the PDF file. Specify as single values (e.g., 3), ranges (e.g., 2-5), or a comma-separated list (e.g., 1,3,6-8).",
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

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    else:
        args.func(args)
        sys.exit(0)
