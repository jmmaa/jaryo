from django.db import models

from api.users.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=4096)
    image_url = models.CharField(max_length=256, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=256, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Draft(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("author", "article")


class Published(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("author", "article")


class EditMapping(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    published = models.ForeignKey(Published, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("draft", "published")
