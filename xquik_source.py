import json
import os
import re
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

SEARCH_URL = "https://xquik.com/api/v1/x/tweets/search"
EXPECTED_COLUMNS = [
    "date",
    "Date",
    "tweet_location",
    "latitude",
    "longitude",
    "hour",
    "day_of_week",
    "month",
    "year",
    "Airline",
    "Predicted_Sentiment",
    "Sentiment_Confidence",
    "retweet_count",
    "like_count",
    "tweet_content",
    "user",
]

AIRLINE_KEYWORDS = {
    "air india": "Air India",
    "indigo": "Indigo",
    "spicejet": "Spicejet",
    "vistara": "Vistara",
    "akasa": "Akasa Air",
    "go first": "Go First",
    "airasia": "AirAsia",
}

POSITIVE_TERMS = {
    "amazing",
    "best",
    "clean",
    "comfortable",
    "easy",
    "fast",
    "friendly",
    "good",
    "great",
    "happy",
    "helpful",
    "love",
    "nice",
    "quick",
    "smooth",
    "thanks",
}

NEGATIVE_TERMS = {
    "angry",
    "bad",
    "broken",
    "cancelled",
    "delay",
    "delayed",
    "dirty",
    "late",
    "lost",
    "missed",
    "poor",
    "rude",
    "slow",
    "terrible",
    "waiting",
    "worst",
}


def load_xquik_posts(query, limit=20):
    """Load recent X posts from Xquik and return dashboard-shaped data."""
    api_key = os.environ.get("XQUIK_API_KEY")
    search_query = query.strip()
    if not api_key or not search_query:
        return None

    bounded_limit = min(max(int(limit), 1), 100)
    params = urlencode({"q": search_query, "queryType": "Latest", "limit": str(bounded_limit)})
    request = Request(
        f"{SEARCH_URL}?{params}",
        headers={"accept": "application/json", "x-api-key": api_key},
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, OSError, TimeoutError, ValueError):
        return None

    return xquik_posts_to_dataframe(_extract_posts(payload))


def xquik_posts_to_dataframe(posts):
    """Map Xquik post dictionaries to the dashboard dataframe contract."""
    rows = []
    for post in posts:
        if not isinstance(post, dict):
            continue

        created_at = _parse_date(_first_value(post, ("createdAt", "created_at", "date", "timestamp")))
        text = str(_first_value(post, ("text", "full_text", "content", "tweet_content")) or "")
        sentiment, confidence = _estimate_sentiment(text)

        rows.append(
            {
                "date": created_at,
                "Date": created_at,
                "tweet_location": _first_value(post, ("location", "tweet_location")) or "Live X",
                "latitude": _first_value(post, ("latitude", "lat")),
                "longitude": _first_value(post, ("longitude", "lng", "lon")),
                "hour": created_at.hour,
                "day_of_week": created_at.strftime("%A"),
                "month": created_at.month,
                "year": created_at.year,
                "Airline": _detect_airline(text),
                "Predicted_Sentiment": sentiment,
                "Sentiment_Confidence": confidence,
                "retweet_count": _metric_value(post, "retweet"),
                "like_count": _metric_value(post, "like"),
                "tweet_content": text,
                "user": _user_value(post),
            }
        )

    data = pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
    if data.empty:
        return data

    data["date"] = pd.to_datetime(data["date"])
    data["Date"] = data["date"]
    data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
    data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")
    data["retweet_count"] = pd.to_numeric(data["retweet_count"], errors="coerce").fillna(0)
    data["like_count"] = pd.to_numeric(data["like_count"], errors="coerce").fillna(0)
    return data


def _extract_posts(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []

    for key in ("tweets", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return value

    data = payload.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("tweets", "items", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return value

    return []


def _first_value(record, keys):
    for key in keys:
        value = record.get(key)
        if value is not None:
            return value
    return None


def _parse_date(value):
    if isinstance(value, datetime):
        return _to_utc_naive(value)
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 9999999999 else value
        return datetime.fromtimestamp(seconds, tz=timezone.utc).replace(tzinfo=None)
    if isinstance(value, str):
        parsed = _parse_date_string(value)
        if parsed is not None:
            return parsed
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _parse_date_string(value):
    normalized = value.replace("Z", "+00:00")
    try:
        return _to_utc_naive(datetime.fromisoformat(normalized))
    except ValueError:
        pass

    for date_format in ("%a %b %d %H:%M:%S %z %Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return _to_utc_naive(datetime.strptime(value, date_format))
        except ValueError:
            pass

    return None


def _to_utc_naive(value):
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _estimate_sentiment(text):
    terms = set(re.findall(r"[a-z']+", text.lower()))
    positive = len(terms & POSITIVE_TERMS)
    negative = len(terms & NEGATIVE_TERMS)
    if positive > negative:
        return "Positive", min(0.95, 0.55 + ((positive - negative) * 0.1))
    if negative > positive:
        return "Negative", min(0.95, 0.55 + ((negative - positive) * 0.1))
    return "Neutral", 0.5


def _detect_airline(text):
    normalized = text.lower()
    for keyword, airline in AIRLINE_KEYWORDS.items():
        if keyword in normalized:
            return airline
    return "Live X"


def _metric_value(post, metric):
    public_metrics = post.get("public_metrics")
    if isinstance(public_metrics, dict):
        value = public_metrics.get(f"{metric}_count")
        if value is not None:
            return value

    for key in (f"{metric}_count", f"{metric}Count", f"{metric}s"):
        value = post.get(key)
        if value is not None:
            return value

    return 0


def _user_value(post):
    author = post.get("author") or post.get("user")
    if isinstance(author, dict):
        return author.get("username") or author.get("screen_name") or author.get("name") or "unknown"
    if author:
        return str(author)
    return post.get("username") or post.get("screen_name") or "unknown"
