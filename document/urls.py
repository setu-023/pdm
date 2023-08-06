from django.urls import path

from .views import *

urlpatterns = [
    path('', DocumentAPIView.as_view()),
    path('<int:pk>', DocumentRetriveAPIView.as_view()),
]
