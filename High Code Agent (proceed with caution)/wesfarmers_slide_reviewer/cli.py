"""CLI helper to run the demo workflow without ADK chat."""

from __future__ import annotations

import argparse
import json

from .tools import list_review_modes, review_presentation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wesfarmers-slide-reviewer",
        description="Wesfarmers BD demo agent utilities.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "modes",
        help="Print available review modes.",
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Execute the review workflow against a presentation.",
    )
    run_parser.add_argument(
        "--presentation-id",
        required=True,
        help="Google Slides presentation ID.",
    )
    run_parser.add_argument(
        "--review-mode",
        required=True,
        help="One of: ic_hard_mode, style_police, ceo_friendly.",
    )
    run_parser.add_argument(
        "--reviewer-name",
        default="Wesfarmers BD Demo Agent",
        help="Name stamped into the output summary.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "modes":
        result = list_review_modes()
    else:
        result = review_presentation(
            presentation_id=args.presentation_id,
            review_mode=args.review_mode,
            reviewer_name=args.reviewer_name,
        )

    print(json.dumps(result, indent=2))
