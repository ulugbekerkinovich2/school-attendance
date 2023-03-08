from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from .views import custom_404_view
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from basic_app import views
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', views.index),
    path('user/', views.ListUsers.as_view()),
    path('user/<int:pk>', views.DetailUsers.as_view()),
    path('student/', views.ListStudent.as_view()),
    path('student/<int:pk>', views.DetailStudent.as_view()),
    path('class/', views.ListSinf.as_view()),
    path('class/<int:pk>', views.DetailSinf.as_view()),
    path('daily/', views.ListBy_Day.as_view()),
    path('daily/<int:pk>', views.DetailBy_Day.as_view()),
    path('data/', views.List.as_view()),
    path('data/<int:pk>', views.Detail.as_view()),

    path('token/', TokenObtainPairView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    # path('swagger/', TemplateView.as_view(template_name='swagger.html', extra_context={'schema_url': 'swagger'})
    #      , name='swagger'),
    # path('openapi', get_schema_view(
    #     title="School Attendance",
    #     description="attendance API",
    #     version="1.0.0"
    # ), name='swagger'),

]
handler404 = custom_404_view
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# urlpatterns += staticfiles_urlpatterns()

# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title='Pastebin API')

# urlpatterns += [
#     path('swaggers/', schema_view)
# ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
