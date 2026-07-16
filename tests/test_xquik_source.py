import unittest

from xquik_source import xquik_posts_to_dataframe


class XquikSourceTest(unittest.TestCase):
    def test_maps_posts_to_dashboard_columns(self):
        data = xquik_posts_to_dataframe(
            [
                {
                    "createdAt": "2026-01-02T03:04:05Z",
                    "text": "IndiGo crew was helpful and the flight was smooth",
                    "author": {"username": "traveler"},
                    "public_metrics": {"like_count": 7, "retweet_count": 2},
                }
            ]
        )

        self.assertEqual(len(data), 1)
        self.assertEqual(data.loc[0, "Airline"], "Indigo")
        self.assertEqual(data.loc[0, "Predicted_Sentiment"], "Positive")
        self.assertEqual(data.loc[0, "like_count"], 7)
        self.assertEqual(data.loc[0, "retweet_count"], 2)
        self.assertEqual(data.loc[0, "user"], "traveler")
        self.assertEqual(data.loc[0, "hour"], 3)

    def test_returns_empty_contract_for_empty_posts(self):
        data = xquik_posts_to_dataframe([])

        self.assertTrue(data.empty)
        self.assertIn("tweet_content", data.columns)
        self.assertIn("Predicted_Sentiment", data.columns)


if __name__ == "__main__":
    unittest.main()
