import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import SearchKeyword, Article

NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news_articles(user, keyword, is_refresh=False):
    """
    Fetches news articles using News API and saves them to the database.
    If is_refresh=True, it only fetches articles newer than the latest saved one.
    """
    # Get or create keyword object
    keyword_obj, created = SearchKeyword.objects.get_or_create(user=user, keyword=keyword)

    # Determine the 'from' date for refresh
    from_date = None
    if is_refresh:
        latest_article = Article.objects.filter(user=user, keyword=keyword).order_by("-published_at").first()
        if latest_article:
            from_date = latest_article.published_at + timedelta(seconds=1)

    params = {
        "q": keyword,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 20,
        "apiKey": settings.NEWS_API_KEY
    }

    if from_date:
        params["from"] = from_date.isoformat()

    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise Exception(f"News API error: {data.get('message')}")

    for article in data.get("articles", []):
        published_at = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
        # Avoid duplicate articles
        if not Article.objects.filter(url=article["url"]).exists():
            Article.objects.create(
                user=user,
                keyword=keyword,
                title=article["title"],
                description=article.get("description", ""),
                url=article["url"],
                published_at=published_at,
                source_name=article["source"]["name"],
                language=article.get("language", "en")
            )
