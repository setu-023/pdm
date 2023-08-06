from django.urls import path
from .views import UserRegisterAPIView, LoginAPIView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view()),
    path('log-in/', LoginAPIView.as_view()),

]
