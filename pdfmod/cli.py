import sys
from argparse import ArgumentParser
from typing import Optional, Sequence

import pdfmod.join


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(
        prog="pdfmod",
        description="pdfmod: iLovePDF made in home.",
        epilog="For help with a specific command, see: `pdfmod <command> -h`.",
    )

    ps_commands = parser.add_subparsers(title="commands", help="PDF Utilities", dest="command")

    # ---------------------------------------------------------------------------------------------
    # 'join' command
    # ---------------------------------------------------------------------------------------------
    ps_join = ps_commands.add_parser("join", help="join the list of pdf files given")
    ps_join.add_argument(
        "input",
        nargs="+",
        help="Input filenames. Use the format 'file.pdf:start-end:password' for optional passwords and page ranges. Example: 'doc.pdf:1-3:myPass'. Leave password or range empty if not needed.",
        metavar="FILE[:START_END[:PASSWORD]]",
    )
    ps_join.add_argument(
        "-o",
        "--output",
        required=True,
        help="output filename",
        metavar="OUTPUT",
    )
    ps_join.set_defaults(func=pdfmod.join.main)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    else:
        args.func(args)
        sys.exit(0)
