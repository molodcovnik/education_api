from django.contrib.auth.models import User
from rest_framework import serializers

from products.models import Product, Lesson, Video, Student


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name',)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title',)


class StudentSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    lesson = serializers.CharField()
    title_video = serializers.CharField()
    url = serializers.URLField()

    is_watched = serializers.BooleanField()
    video_view_counter = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ('product', 'lesson', 'title_video', 'url', 'is_watched', 'video_view_counter', )
