from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', FileUploadView.as_view())
]