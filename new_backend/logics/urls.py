from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', LogicView.as_view())
]