from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def is_voted(self, user):
        return self.vote.filter(pk=user.pk).exists()

class Reply(models.Model):
    comment = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted')
    def is_voted(self, user):
        return self.vote.filter(pk=user.pk).exists()
