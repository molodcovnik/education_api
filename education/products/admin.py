from django.contrib import admin

from .models import Video, Product, Lesson, Student

# Register your models here.
admin.site.register(Video)
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Student)
