import datetime

from django.db.models import Q
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response

from basic_app import models, serializer
from davomat_ import daily, daily1


# Create your views here.

class ListUsers(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializer.UserSerializer1


class DetailUsers(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializer.UserPasswordSerializer


class ListStudent(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializer.StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializer.StudentSerializer


class ListSinf(generics.ListCreateAPIView):
    queryset = models.Sinf.objects.all()
    serializer_class = serializer.SinfSerializer


class DetailSinf(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Sinf.objects.all()
    serializer_class = serializer.SinfSerializer


class ListBy_Day(generics.ListAPIView):
    queryset = models.ByDay.objects.all()
    serializer_class = serializer.ByDaySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['created_at']


class DetailBy_Day(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ByDay.objects.all()
    serializer_class = serializer.ByDaySerializer


class List(generics.ListCreateAPIView):
    queryset = models.DataStudents.objects.all()
    serializer_class = serializer.DataSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['weekday']

    def perform_create(self, serializer):
        instance = serializer.save()
        daily()


class Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DataStudents.objects.all()
    serializer_class = serializer.DataSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     # Call your function here with the retrieved instance
    #     daily()
    #
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
