from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse




class Post(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,default=1)
    title = models.CharField(max_length=125)
    content = models.TextField()
    post_image = models.ImageField()
    updated = models.DateTimeField(auto_now=True, auto_now_add= False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add= True)
    date = models.DateField(default=timezone.now)




    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


    class Meta:
        ordering = ["-timestamp", "-updated"]



