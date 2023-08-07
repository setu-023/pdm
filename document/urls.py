from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', DocumentRetriveAPIView.as_view()),
    path('meta-data/<int:pk>', MetadataAPIView.as_view()),
    path('share', FileSharingAPIView.as_view()),
    # path('shared-file', ViewFileSharingAPIView.as_view()),
    path('search/', SearchAPI.as_view()),
    path('', DocumentAPIView.as_view()), 


]
