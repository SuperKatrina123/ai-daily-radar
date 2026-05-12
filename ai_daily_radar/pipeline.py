"""Transform AI HOT items into an application-layer daily radar."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any


APPLICATION_KEYWORDS = (
    "agent",
    "agents",
    "app",
    "apps",
    "api",
    "automation",
    "browser",
    "canvas",
    "chatbot",
    "coding",
    "copilot",
    "crm",
    "design",
    "developer",
    "devtool",
    "figma",
    "gmail",
    "ide",
    "image",
    "integration",
    "mcp",
    "notebook",
    "obsidian",
    "office",
    "product",
    "saas",
    "slack",
    "telegram",
    "tool",
    "tools",
    "video",
    "workflow",
    "write",
    "应用",
    "产品",
    "工具",
    "工作流",
    "自动化",
    "智能体",
    "代理",
    "办公",
    "写作",
    "编程",
    "设计",
    "视频",
    "图像",
    "浏览器",
    "插件",
    "集成",
    "创作",
    "开发者",
    "客服",
)

TREND_PATTERNS = (
    ("agentic_workflows", ("agent", "agents", "智能体", "代理", "自动化", "workflow", "工作流")),
    ("multimodal_creation", ("image", "video", "audio", "canvas", "图像", "视频", "语音", "多模态", "创作")),
    ("developer_tools", ("coding", "code", "ide", "developer", "api", "mcp", "编程", "代码", "开发者")),
    ("enterprise_ops", ("enterprise", "saas", "crm", "office", "slack", "gmail", "企业", "办公", "协作")),
    ("personal_productivity", ("notebook", "obsidian", "browser", "search", "write", "知识", "浏览器", "写作")),
)

TREND_LABELS = {
    "agentic_workflows": "Agent 化工作流从演示走向可落地任务",
    "multimodal_creation": "多模态创作能力继续产品化",
    "developer_tools": "开发者工具正在把 AI 融入日常操作链",
    "enterprise_ops": "企业和办公场景更重视流程集成",
    "personal_productivity": "个人效率工具开始围绕上下文和知识库重组",
}

MARKET_NEWS_KEYWORDS = ("ipo", "上市", "股票", "发行价", "认购", "筹资", "融资", "市值")


@dataclass(frozen=True)
class RadarReport:
    generated_at: datetime
    window_hours: int
    source_count: int
    deduped_count: int
    application_count: int
    items: list[dict[str, Any]]
    trends: list[str]
    practice_plan: list[str]


def build_report(items: list[dict[str, Any]], window_hours: int = 24) -> RadarReport:
    deduped = dedupe_items(items)
    application_items = filter_application_layer(deduped)
    trend_keys = detect_trends(application_items)
    trends = [TREND_LABELS[key] for key in trend_keys]
    practice_plan = build_practice_plan(application_items, trends)
    return RadarReport(
        generated_at=datetime.now(timezone.utc),
        window_hours=window_hours,
        source_count=len(items),
        deduped_count=len(deduped),
        application_count=len(application_items),
        items=application_items,
        trends=trends,
        practice_plan=practice_plan,
    )


def dedupe_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        key = _dedupe_key(item)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def filter_application_layer(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    fallback: list[dict[str, Any]] = []

    for item in items:
        category = str(item.get("category") or "")
        text = _search_text(item)
        if category == "industry" and _contains_any(text, MARKET_NEWS_KEYWORDS):
            continue
        if category == "ai-products" or _contains_any(text, APPLICATION_KEYWORDS):
            matched.append(item)
        elif category in {"tip", "industry"}:
            fallback.append(item)

    return matched or fallback[:10]


def detect_trends(items: list[dict[str, Any]], limit: int = 3) -> list[str]:
    scores: Counter[str] = Counter()
    for item in items:
        text = _search_text(item)
        for key, keywords in TREND_PATTERNS:
            if _contains_any(text, keywords):
                scores[key] += 1

    if not scores:
        return ["personal_productivity"]

    return [key for key, _ in scores.most_common(limit)]


def build_practice_plan(items: list[dict[str, Any]], trends: list[str]) -> list[str]:
    focus = _pick_focus_item(items)
    title = focus.get("title") if focus else "今天最值得试的应用层变化"
    source = focus.get("source") if focus else "AI HOT"

    return [
        f"选一个与你当前工作流最接近的场景，围绕「{title}」写下 1 个可验证的小假设。",
        "用 30 分钟做一个最小原型：输入固定样例、产出固定格式，不追求自动化闭环。",
        "记录 3 个指标：节省时间、输出质量、是否愿意明天继续用。",
        f"把验证结果沉淀成一条模板或 checklist，并标注来源：{source}。",
    ]


def _pick_focus_item(items: list[dict[str, Any]]) -> dict[str, Any]:
    if not items:
        return {}
    priority = {"ai-products": 0, "tip": 1, "industry": 2, "ai-models": 3, "paper": 4}
    return min(items, key=lambda item: priority.get(str(item.get("category") or ""), 9))


def _dedupe_key(item: dict[str, Any]) -> str:
    url = str(item.get("url") or "").strip().lower()
    if url:
        return url
    title = normalize_text(str(item.get("title") or item.get("title_en") or ""))
    source = normalize_text(str(item.get("source") or ""))
    return f"{source}:{title}"


def _search_text(item: dict[str, Any]) -> str:
    parts = [
        item.get("title"),
        item.get("title_en"),
        item.get("summary"),
        item.get("source"),
        item.get("category"),
    ]
    return normalize_text(" ".join(str(part) for part in parts if part))


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword.lower() in text for keyword in keywords)
