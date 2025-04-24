from django.shortcuts import render, redirect
import requests
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from .models import SearchKeyword, NewsArticle


def search_news(request):
    """
    View to handle the search functionality for news articles.
    It fetches news articles based on the keyword provided by the user.
    """

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
      
        # Check if the keyword already exists for the user
        search_obj, created = SearchKeyword.objects.get_or_create(user=request.user, keyword=keyword)

        # if the keyword already exists and the last fetch was within 15 minutes, redirect to search history
        if not created and now() - search_obj.latest_fetched < timedelta(minutes=15):
            return redirect('search_history')
        
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params={'q': keyword, 'apiKey': settings.NEWS_API_KEY}
        )
        articles = response.json().get('articles', [])

        # Check if the response is valid
        NewsArticle.objects.filter(keyword=search_obj).delete()

        # create new articles for the keyword
        for article in articles:
            NewsArticle.objects.create(
                keyword=search_obj,
                title=article['title'],
                description=article.get('description', ''),
                url=article['url'],
                published_at=article['publishedAt'],
                source=article['source']['name'],
                language=article.get('language', 'en')
            )
        return redirect('search_history')

    return render(request, 'news/search.html')    

def search_history(request):
    searches = SearchKeyword.objects.filter(user=request.user).order_by('-last_fetched')
    return render(request, 'news/history.html', {'searches': searches})