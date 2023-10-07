from django.contrib.auth.models import User
from django.db import models

from embed_video.fields import EmbedVideoField

class Video(models.Model):
    title = models.CharField(max_length=128)
    added = models.DateTimeField(auto_now_add=True)
    url = EmbedVideoField()
    duration = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.url[0:123]} {self.owner} {self.duration}'

    class Meta:
        ordering = ['-added']


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='views', blank=True, on_delete=models.PROTECT, default=None)
    is_watched = models.BooleanField(default=False)
    video_view_counter = models.IntegerField(default=0)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f'{self.user} {self.video} {self.is_watched}'

    def watched(self):
        self.is_watched = True
        self.save()


class Lesson(models.Model):
    name = models.TextField(max_length=1024)
    video = models.ManyToManyField(Video, related_name='videos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.video} {self.owner}'


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    subscribers = models.ManyToManyField(User, related_name='products', blank=True)
    lessons = models.ManyToManyField(Lesson, related_name='courses', blank=True)

    def __str__(self):
        return f'{self.name} {self.owner} {self.created} {self.subscribers} {self.lessons}'
