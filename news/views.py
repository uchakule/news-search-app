from django.shortcuts import render, redirect
import requests
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.conf import settings
from .models import SearchKeyword, Article
from .forms import KeywordSearchForm
from .utils import fetch_news_articles
from django.contrib import messages

NEWS_API_KEY = settings.NEWS_API_KEY

def fetch_articles(keyword, from_date=None):
    params = {
        'q': keyword,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 20
    }
    if from_date:
        params['from'] = from_date.isoformat()

    response = requests.get('https://newsapi.org/v2/everything', params=params)
    return response.json().get('articles', [])

@login_required
def search_news(request):
    """
    View to handle the search functionality for news articles.
    It fetches news articles based on the keyword provided by the user.
    """
    form = KeywordSearchForm(request.POST or None)
    articles = []

    if request.method == 'POST' and form.is_valid():
        keyword = form.cleaned_data['keyword']
        user_keywords = SearchKeyword.objects.filter(user=request.user, keyword__iexact=keyword)
      
        # Check if keyword exists already
        if user_keywords.exists():
            search = user_keywords.first()
            time_since = now() - search.last_searched_at if search.last_searched_at else timedelta(hours=1)
            if time_since < timedelta(minutes=15):
                articles = list(search.articles.all().order_by('-published_at'))
            else:
                new_articles = fetch_articles(keyword, search.last_searched_at)
                for art in new_articles:
                    Article.objects.create(
                        keyword=search,
                        title=art['title'],
                        description=art.get('description', ''),
                        url=art['url'],
                        source_name=art['source']['name'],
                        published_at=art['publishedAt'],
                        language=art.get('language', 'en')
                    )
                search.last_searched_at = now()
                search.save()
                articles = list(search.articles.all().order_by('-published_at'))
        else:
            search = SearchKeyword.objects.create(user=request.user, keyword=keyword, last_searched_at=now())
            new_articles = fetch_articles(keyword)
            for art in new_articles:
                Article.objects.create(
                    keyword=search,
                    title=art['title'],
                    description=art.get('description', ''),
                    url=art['url'],
                    source=art['source']['name'],
                    published_at=art['publishedAt'],
                    language=art.get('language', 'en')
                )
            articles = list(search.articles.all().order_by('-published_at'))

    return render(request, 'news/search.html', {'form': form, 'articles': articles})

@login_required
def refresh_news(request, keyword):
    try:
        # Get the latest stored date for this keyword
        keyword_obj = SearchKeyword.objects.filter(user=request.user, keyword=keyword).first()
        if keyword_obj:
            # Call utility function to fetch and store new articles
            fetch_news_articles(request.user, keyword, is_refresh=True)
            messages.success(request, f"News articles for '{keyword}' have been refreshed.")
        else:
            messages.error(request, f"No saved keyword found for '{keyword}'.")
    except Exception as e:
        messages.error(request, f"Error while refreshing news: {e}")

    return redirect("news:search_history")    

@login_required
def history(request):
    searches = SearchKeyword.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'news/history.html', {'searches': searches})