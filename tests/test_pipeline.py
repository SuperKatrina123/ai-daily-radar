import unittest

from ai_daily_radar.pipeline import build_report, dedupe_items, filter_application_layer
from ai_daily_radar.renderer import render_markdown


class PipelineTest(unittest.TestCase):
    def test_dedupe_prefers_unique_urls(self):
        items = [
            {"title": "A", "url": "https://example.com/a", "source": "X"},
            {"title": "A again", "url": "https://example.com/a", "source": "Y"},
            {"title": "B", "url": "https://example.com/b", "source": "X"},
        ]

        self.assertEqual(len(dedupe_items(items)), 2)

    def test_filter_application_layer_keeps_products_and_workflows(self):
        items = [
            {"title": "New model benchmark", "category": "ai-models", "summary": "faster tokens"},
            {"title": "AI chip company IPO", "category": "industry", "summary": "stock price and financing"},
            {"title": "Agent workflow tool launches", "category": "industry", "summary": "automation for teams"},
            {"title": "AI writing app update", "category": "ai-products", "summary": "new editor"},
        ]

        filtered = filter_application_layer(items)

        self.assertEqual(
            [item["title"] for item in filtered],
            [
                "Agent workflow tool launches",
                "AI writing app update",
            ],
        )

    def test_render_markdown_contains_practice_first_context(self):
        items = [
            {
                "title": "AI coding agent ships browser automation",
                "url": "https://example.com/agent",
                "source": "Example",
                "category": "ai-products",
                "summary": "A coding agent adds browser workflow automation.",
                "publishedAt": "2026-05-09T08:00:00.000Z",
            }
        ]
        report = build_report(items)

        markdown = render_markdown(report, prompt_text="prompt")

        self.assertIn("## 今天的最小实践方案", markdown)
        self.assertIn("Agent 化工作流", markdown)
        self.assertIn("https://example.com/agent", markdown)


if __name__ == "__main__":
    unittest.main()
