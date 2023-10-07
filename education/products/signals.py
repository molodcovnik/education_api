from pprint import pprint

from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Product, Student, Video


@receiver(m2m_changed, sender=Product.subscribers.through)
def subscribers_changed(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        user = list(kwargs['pk_set'])[0]
        print(user)
        user = User.objects.get(id=user)
        # print(kwargs['pk_set'])
        product_name = instance.name
        subscribers = list(Product.objects.filter(name=product_name).values_list('subscribers', flat=True))
        if user not in subscribers:
            videos = list(Product.objects.filter(name=product_name).values_list('lessons__video', flat=True))
            for video in videos:
                student = Student.objects.create(user=user, video=Video.objects.get(id=video))
                student.save()


