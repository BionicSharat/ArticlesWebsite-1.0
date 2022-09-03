from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class Categories(models.Model):
    title = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=10000)
    year_created = models.IntegerField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    categories = models.ManyToManyField(Categories)
    
    def __str__(self):
        return self.title

class User_article(models.Model):
    username = models.CharField(max_length=500, blank=False)
    articles_user = models.ManyToManyField(Article)
    user_linked = models.OneToOneField(User, on_delete=models.CASCADE)
    categories_user = models.ManyToManyField(Categories)
    article_profile_pic = models.ImageField(upload_to=filepath, null=True, blank=True, default=r'article\default_imgs\user-d-i.png')

    def __str__(self):
        return self.username

class Collections(models.Model):
    title = models.CharField(max_length=70, blank=False)
    admins = models.ManyToManyField(User_article, related_name='admins', blank=False)
    readers = models.ManyToManyField(User_article, related_name='readers', blank=False)
    participants = models.ManyToManyField(User_article, related_name='participants', blank=False)
    writers = models.ManyToManyField(User_article, related_name='writers', blank=False)
    articles = models.ManyToManyField(Article, blank=False)
    categories = models.ManyToManyField(Categories, blank=False)


    def __str__(self):
        return self.title