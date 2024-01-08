from django.urls import path

from . import views

urlpatterns = [
    path("index/", view=views.index),
]
