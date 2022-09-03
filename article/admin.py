from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Article)
admin.site.register(Categories)
admin.site.register(User_article)
admin.site.register(Collections)