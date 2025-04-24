import datetime
from .models import SearchKeyword
from .utils import fetch_news_articles  # Assume this handles News API fetching logic

def refresh_all_keywords():
    keywords = SearchKeyword.objects.all()
    for keyword_obj in keywords:
        fetch_news_articles(keyword_obj.user, keyword_obj.keyword, is_background=True)
