from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)

class Post(models.Model):
    user_post= models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,default=1)
    title = models.CharField(max_length=125)
    content = models.TextField()
    post_image = models.ImageField()
    updated = models.DateTimeField(auto_now=True, auto_now_add= False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add= True)
    date = models.DateField(default=timezone.now)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')



    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


    class Meta:
        ordering = ["-timestamp", "-updated"]

# class User(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)
#     author = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blog_post', default=1)
#
#     def __unicode__(self):
#         return self.author
#
#     def __str__(self):
#         return self.author


