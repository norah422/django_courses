from django.db import models
from django.contrib.auth.models import User 

class Post(models.Model):
    title_en = models.CharField(max_length=200, verbose_name='Post Title (english)')
    title_ar = models.CharField(max_length=200, verbose_name='Post Title (arabic)')

    content_en = models.TextField(verbose_name='Post Content (english)')
    content_ar = models.TextField(verbose_name='Post Content (arabic)')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')

    image = models.ImageField(upload_to='blog_images/', verbose_name='Post Image', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ar