from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class SearchKeyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    latest_fetched = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_searched_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.keyword} - {self.user.username}"

class Article(models.Model):
    keyword = models.ForeignKey(SearchKeyword, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.CharField(max_length=255)
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return self.title    