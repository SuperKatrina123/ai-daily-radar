"""Markdown rendering for AI Daily Radar reports."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .pipeline import RadarReport


CATEGORY_LABELS = {
    "ai-models": "模型能力",
    "ai-products": "产品与应用",
    "industry": "行业与平台",
    "paper": "论文研究",
    "tip": "技巧与观点",
}


def render_markdown(report: RadarReport, prompt_text: str = "", timezone_name: str = "Asia/Shanghai") -> str:
    display_tz = _load_timezone(timezone_name)
    local_generated = report.generated_at.astimezone(display_tz)
    lines = [
        f"# AI Daily Radar · {local_generated:%Y-%m-%d}",
        "",
        f"- 时间窗：过去 {report.window_hours} 小时",
        f"- 原始条目：{report.source_count}，去重后：{report.deduped_count}，应用层相关：{report.application_count}",
        "- 主题：AI 应用层趋势 → 今天能做什么实践",
        "",
        "## 2-3 个趋势",
        "",
    ]

    if report.trends:
        for trend in report.trends[:3]:
            lines.append(f"- {trend}")
    else:
        lines.append("- 今天应用层信号较弱，适合复盘已有工具链而不是追新。")

    lines.extend(["", "## 今天的最小实践方案", ""])
    for index, step in enumerate(report.practice_plan, 1):
        lines.append(f"{index}. {step}")

    lines.extend(["", "## 应用层信号", ""])
    if report.items:
        for index, item in enumerate(report.items, 1):
            lines.extend(_render_item(index, item, display_tz))
    else:
        lines.append("今天没有筛出足够明确的应用层条目。")

    lines.extend(
        [
            "",
            "## 后续推送接口预留",
            "",
            "- 邮件：把本文件内容作为纯 Markdown 邮件正文发送。",
            "- Telegram：把趋势和最小实践方案截短为消息摘要，附上本地报告路径或仓库链接。",
            "- 飞书：把本文件 Markdown 转成云文档或群消息。",
            "- Obsidian：把 `data/reports/latest.md` 同步到 vault 的 Daily Notes 目录。",
            "",
            "## 生成说明",
            "",
            f"- 生成时间：{_format_time(report.generated_at, display_tz)}",
            "- 数据来自 AI HOT 精选条目。",
        ]
    )

    if prompt_text:
        lines.extend(["- Prompt：`prompts/ai_daily_radar.md`"])

    lines.append("")
    return "\n".join(lines)


def save_report(markdown: str, output_path: Path, archive_dir: Path | None = None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    if archive_dir is not None:
        archive_dir.mkdir(parents=True, exist_ok=True)
        date_suffix = datetime.now().strftime("%Y-%m-%d")
        archive_path = archive_dir / f"{date_suffix}.md"
        archive_path.write_text(markdown, encoding="utf-8")


def _render_item(index: int, item: dict[str, Any], display_tz: ZoneInfo = ZoneInfo("Asia/Shanghai")) -> list[str]:
    title = str(item.get("title") or item.get("title_en") or "未命名条目").strip()
    source = str(item.get("source") or "未知来源").strip()
    category = CATEGORY_LABELS.get(str(item.get("category") or ""), "其他")
    summary = str(item.get("summary") or "").strip()
    url = str(item.get("url") or "").strip()
    published = _format_item_time(item.get("publishedAt"), display_tz)

    lines = [f"{index}. **{title}** — {source}（{category}）"]
    if published:
        lines.append(f"   {published}")
    if summary:
        lines.append(f"   {summary}")
    if url:
        lines.append(f"   {url}")
    lines.append("")
    return lines


def _format_item_time(value: Any, display_tz: ZoneInfo) -> str:
    if not value:
        return ""
    if not isinstance(value, str):
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return _format_time(parsed, display_tz)


def _format_time(value: datetime, display_tz: ZoneInfo) -> str:
    local_value = value.astimezone(display_tz)
    return local_value.strftime("%Y-%m-%d %H:%M %Z")


def _load_timezone(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return ZoneInfo("Asia/Shanghai")
