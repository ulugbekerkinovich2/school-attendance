
from django.db.models.functions import TruncMonth
from django.db.models import  Count
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters

from basic_app import models, serializer
from basic_app.models import ByDay
from davomat_ import daily, daily_new


# Create your views here.
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


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

    # def get_queryset(self):
    #     byday_month = ByDay.objects.annotate(month=TruncMonth('created_at'))
    #     byday_month_count = byday_month.values('month').annotate(count=Count('id'))
    #     byday_month_count = byday_month_count.order_by('-count')
    #
    #     largest_month = byday_month_count.first()['month']
    #     largest_month_year = largest_month.year
    #     largest_month_month = largest_month.month
    #
    #     byday_largest_month = ByDay.objects.filter(created_at__month=largest_month_month,
    #                                                created_at__year=largest_month_year)
    #
    #     return byday_largest_month


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
        daily_new()
        return instance


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


def index(request):
    return render(request, 'index.html')
