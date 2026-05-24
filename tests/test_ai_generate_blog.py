import tempfile
import unittest
from pathlib import Path

from ai_generate_blog import build_slug, select_topic


class TopicSelectionTest(unittest.TestCase):
    def test_select_topic_skips_today_existing_posts(self):
        with tempfile.TemporaryDirectory() as tmp:
            posts_dir = Path(tmp)
            topics = ["Java 架构实践", "网络排障手册"]
            (posts_dir / f"2026-05-24-{build_slug(topics[0])}.md").write_text("", encoding="utf-8")

            topic = select_topic(topics, "2026-05-24", posts_dir)

            self.assertEqual(topic, topics[1])

    def test_select_topic_prefers_least_recently_used_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            posts_dir = Path(tmp)
            topics = ["Java 架构实践", "网络排障手册", "数据治理复盘"]
            (posts_dir / f"2026-05-20-{build_slug(topics[0])}.md").write_text("", encoding="utf-8")
            (posts_dir / f"2026-05-23-{build_slug(topics[1])}.md").write_text("", encoding="utf-8")

            topic = select_topic(topics, "2026-05-24", posts_dir)

            self.assertEqual(topic, topics[2])


if __name__ == "__main__":
    unittest.main()
