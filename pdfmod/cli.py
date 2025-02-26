import sys
from argparse import ArgumentParser
from typing import Optional, Sequence

import pdfmod.cat
import pdfmod.rm


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(
        prog="pdfmod",
        description="pdfmod: iLovePDF made in home.",
        epilog="For help with a specific command, see: `pdfmod <command> -h`.",
    )

    ps_commands = parser.add_subparsers(title="commands", help="PDF Utilities", dest="command")

    # ---------------------------------------------------------------------------------------------
    # 'cat' command
    # ---------------------------------------------------------------------------------------------
    ps_cat = ps_commands.add_parser(
        "cat", help="Merge a list of PDF files into a single document"
    )
    ps_cat.add_argument(
        "input",
        nargs="+",
        help="Path(s) to one or more input PDF files. Use the format 'file.pdf:start-end:password' for optional passwords and page ranges. Example: 'doc.pdf:1-3:myPass'. Leave password or range empty if not needed",
        metavar="FILE[:START_END[:PASSWORD]]",
    )
    ps_cat.add_argument(
        "-o",
        "--output",
        nargs="?",
        help="Output filename",
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
        "path",
        help="Path to the input PDF file.",
        metavar="PATH",
    )
    ps_rm.add_argument(
        "pages",
        help="Pages to remove from the PDF file. Specify as single values (e.g., 3), ranges (e.g., 2-5), or a comma-separated list (e.g., 1,3,6-8).",
        metavar="PAGES",
    )
    ps_rm.add_argument(
        "-o",
        "--output",
        nargs="?",
        help="Output filename",
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
