"""Command line for shopify-cod-store-tools.

Examples:
    python -m store_tools.cli label in.jpg out.jpg --color "Polo Blue"
    python -m store_tools.cli check-order order.json
    python -m store_tools.cli returns orders.csv
"""

import argparse
import json
import sys

from .image_label import label_image
from .order_check import check_order, format_order_summary
from .returns import analyse_csv


def main(argv=None):
    parser = argparse.ArgumentParser(prog="store-tools")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("label", help="Label a product image with its colour")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--color", required=True)
    p.add_argument("--corner", default="bottom-left",
                   choices=["bottom-left", "bottom-right"])

    p = sub.add_parser("check-order", help="Check a COD order JSON file")
    p.add_argument("file")
    p.add_argument("--country", default=None,
                   help="Country code, e.g. PK, IN, BD, NG, EG, AE")

    p = sub.add_parser("returns", help="Return rate from an orders CSV")
    p.add_argument("file")

    args = parser.parse_args(argv)
    if args.command == "label":
        print(label_image(args.input, args.output, args.color,
                          corner=args.corner))
    elif args.command == "check-order":
        with open(args.file, encoding="utf-8") as handle:
            order = json.load(handle)
        problems = check_order(order, country_code=args.country)
        print(format_order_summary(order, country_code=args.country))
        if problems:
            print("PROBLEMS:")
            for problem in problems:
                print(f" - {problem}")
            return 1
        print("OK: passes the COD checklist.")
    elif args.command == "returns":
        print(json.dumps(analyse_csv(args.file), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
