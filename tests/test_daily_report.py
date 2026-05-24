import unittest

from fetch_daily_report import parse_feed


class DailyReportFeedTest(unittest.TestCase):
    def test_parse_feed_reads_latest_items(self):
        xml_text = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <item>
      <title>AI 日报 2026-05-24</title>
      <link>https://example.com/daily/1</link>
      <description><![CDATA[今日重点：模型与工具更新。]]></description>
      <pubDate>Sun, 24 May 2026 08:00:00 +0800</pubDate>
    </item>
  </channel>
</rss>
"""

        items = parse_feed(xml_text, limit=5)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "AI 日报 2026-05-24")
        self.assertEqual(items[0]["link"], "https://example.com/daily/1")
        self.assertIn("模型与工具更新", items[0]["description"])


if __name__ == "__main__":
    unittest.main()
