from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchKeyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    latest_fetched = models.DateTimeField(auto_now=True)

class NewsArticle(models.Model):
    keyword = models.ForeignKey(SearchKeyword, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.CharField(max_length=255)
    language = models.CharField(max_lenght=10, default='en')    