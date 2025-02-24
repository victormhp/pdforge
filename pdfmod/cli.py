from argparse import ArgumentParser

import pdfmod.merge


def show_version():
    print(f"{pdfmod.__app__} v{pdfmod.__version__}")


def main():
    parser = ArgumentParser(
        prog="pdfmod",
        description="pdfmod: iLovePDF made in home.",
        epilog="For help with a specific command, see: `pdfmod <command> -h`.",
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="show the application's version and exit"
    )

    commands_parser = parser.add_subparsers(title="commands", help="PDF Utilities", dest="command")

    merge_parser = commands_parser.add_parser("merge", help="Merge the list of pdf files given")
    merge_parser.add_argument("files", nargs="+", help="List of PDF files to merge")
    merge_parser.add_argument(
        "-o",
        "--output",
        default="merged.pdf",
        help="Output file path",
        metavar="FILE",
    )

    args = parser.parse_args()

    if args.version:
        show_version()
    elif args.command == "merge":
        pdfmod.merge.main(args.files, args.output)
    else:
        parser.print_help()
