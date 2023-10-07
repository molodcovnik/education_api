import json
from itertools import chain

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Sum, F, Q, FilteredRelation, Count, OuterRef
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from rest_framework import viewsets, generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from api.serializers import StudentSerializer

from products.models import Product, Lesson, Video, Student


# class PostView(APIView):
#     def get(self, request, format=None):
#         user = self.request.user
#         products = user.products.all()
#         # data = {
#         #     'products': products.values(),
#         #
#         # }
#         # return JsonResponse(data)
#         serialized_data = serialize("json", products)
#         serialized_data = json.loads(serialized_data)
#         return Response(serialized_data)


# class ProductsView(APIView):
#
#     def get(self, request, format=None):
#         user = self.request.user
#
#         accesses = user.products.all()
#
#         data = {"lessons": list(Product.objects.filter(lessons__in=accesses.values('lessons')).values(
#             'lessons__name',
#             'lessons__video__title',
#             'lessons__video__views__is_watched',
#             'lessons__video__views__video_view_counter'))}
#
#
#         return Response(data, )

class LessonsView(APIView):

    def get(self, request, format=None):
        data = list(Student.objects.filter(user=self.request.user)
                    .annotate(
            product=F('video__videos__courses__name'),
            title_video=F('video__title'),
            url=F('video__url'),
            lesson=F('video__videos__name')
        )
                    .values('product', 'title_video', 'url', 'lesson', 'is_watched', 'video_view_counter'))

        serializer = StudentSerializer(data, many=True)

        return Response(serializer.data)


class LessonsProductView(APIView):

    def get(self, request, format=None, **kwargs):
        user = self.request.user
        products_user = user.products.all().values_list('id', flat=True)
        try:
            course = Product.objects.get(id=kwargs['pk'])
        except:
            raise Http404

        if course.id in products_user:
            videos = course.lessons.all().values_list('video__id', flat=True)

            data = list(
                Student.objects.filter(user=user, video__in=videos)
                .annotate(
                    product=F('video__videos__courses__name'),
                    title_video=F('video__title'),
                    url=F('video__url'),
                    lesson=F('video__videos__name')
                )
                .values('product', 'title_video', 'url', 'lesson', 'is_watched', 'video_view_counter')
                )

            serializer = StudentSerializer(data, many=True)
            return Response(serializer.data)
        return Response(data={
            "error": "Вы не являетесь подписчиком данного продукта"
            })


class StaticsView(APIView):
    def get(self, request, format=None):
        data = Product.objects.all().annotate(
            lesson_view_count=Count(
                Student.objects.filter(
                    video=OuterRef('id'),
                    is_watched=True
                ).values('id')
            )
        )

        return Response(data={
            "data": data
        })

# qs = Student.objects.filter(is_watched=True).count()

# хороший вариант
# class PostView(APIView):
#     def get(self, request, format=None):
#         user = self.request.user
#         products = user.products.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

# class PostView(APIView):
#     def get(self, request, format=None):
#         user = self.request.user.id
#         products = set(Product.objects.filter(subscribers__id=user).values_list('lessons__name',))
#         data = {
#             'lessosns': list(products),
#              }
#         return Response(data)

# class PostView(APIView):
#     def get(self, request, format=None):
#         user = self.request.user.id
#         lessons = set(Product.objects.filter(subscribers__id=user).values_list('lessons__name',))
#         videos = set(Student.objects.filter(user=user).values_list('video__title', 'is_watched'))
#         data = {
#             'lessosns': {
#                 "name": (lesson for lesson in lessons),
#                 "video": (video for video in videos)
#                 },
#              }
#         return Response(data)

# class PostView(APIView):
#     def get(self, request, format=None):
#         user = self.request.user.id
#         lessons = set(Product.objects.filter(subscribers__id=user).values_list('lessons__name',))
#         videos = set(Student.objects.filter(user=user).values_list('video__title' ,'is_watched'))
#
#         model_combination = list(chain(lessons, videos))
#         serialized_data = serialize("json", model_combination)
#         serialized_data = json.loads(serialized_data)
#         return Response(model_combination)

#
# user = User.objects.get(id=self.request.user)
# products = user.products.all()
# qs = Product.objects.filter(
#      lessons__in=products.values('lessons')
#     ).alias(
#         videos=FilteredRelation(
#             'subscribers__student',
#             condition=Q(subscribers__student=self.request.user)
#         )
#     ).annotate(
#      is_watched=F('subscribers__student__is_watched'),
#      video_view_counter=F('subscribers__student__video_view_counter')
#     )
#
# accesses = tim.products.values('name')
