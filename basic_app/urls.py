from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from basic_app import views

urlpatterns = [
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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()