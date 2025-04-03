from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("index/", views.index, name="index"),
    path("/fitnessTrackerApp/5/", views.detail, name="detail"),
    path("/fitnessTrackerApp/5/results", views.results, name="results"),
    path("/fitnessTrackerApp/5/vote/", views.vote, name="vote"),
]