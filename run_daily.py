#!/usr/bin/env python3
"""Run the AI Daily Radar workflow."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from ai_daily_radar.aihot_client import AihotClientError, fetch_selected_items
from ai_daily_radar.pipeline import build_report
from ai_daily_radar.renderer import render_markdown, save_report


ROOT = Path(__file__).resolve().parent
DEFAULT_PROMPT = ROOT / "prompts" / "ai_daily_radar.md"
DEFAULT_OUTPUT = ROOT / "data" / "reports" / "latest.md"
DEFAULT_ARCHIVE = ROOT / "data" / "reports" / "archive"


def main() -> int:
    args = parse_args()
    prompt_text = read_prompt(args.prompt)

    try:
        items = load_items(args)
        report = build_report(items, window_hours=args.hours)
        markdown = render_markdown(report, prompt_text=prompt_text, timezone_name=args.timezone)
        save_report(markdown, args.output, archive_dir=args.archive_dir if args.archive else None)
    except AihotClientError as exc:
        print(f"AI Daily Radar failed: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"AI Daily Radar failed while reading or writing files: {exc}", file=sys.stderr)
        return 1

    print(f"AI Daily Radar report written to {args.output}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI Daily Radar Markdown report.")
    parser.add_argument("--hours", type=int, default=24, help="Rolling window in hours. Default: 24.")
    parser.add_argument("--take", type=int, default=100, help="Maximum AI HOT items to fetch. Default: 100.")
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT, help="Prompt file path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Markdown report output path.")
    parser.add_argument("--archive", action="store_true", help="Also save a dated report snapshot.")
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE, help="Directory for dated snapshots.")
    parser.add_argument("--input-json", type=Path, help="Use a local AI HOT response JSON file instead of fetching.")
    parser.add_argument(
        "--timezone",
        default=os.getenv("AI_DAILY_RADAR_TZ", "Asia/Shanghai"),
        help="Display timezone for report timestamps. Default: Asia/Shanghai.",
    )
    return parser.parse_args()


def read_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_items(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.input_json:
        payload = json.loads(args.input_json.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            items = payload.get("items", [])
        else:
            items = payload
        if not isinstance(items, list):
            raise AihotClientError("Local input JSON must be a list or an object with an items list.")
        return [item for item in items if isinstance(item, dict)]

    return fetch_selected_items(hours=args.hours, take=args.take)


if __name__ == "__main__":
    raise SystemExit(main())
