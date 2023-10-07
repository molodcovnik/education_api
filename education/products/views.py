from django.shortcuts import render

from .models import Video

def index(request):
    video = Video.objects.all()
    return render(request, 'products/index.html', context={'videos': video})
