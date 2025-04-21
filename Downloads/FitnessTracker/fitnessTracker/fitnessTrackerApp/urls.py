from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("index/", views.index, name="index"),
    path("/fitnessTrackerApp/5/", views.detail, name="detail"),
    path("/fitnessTrackerApp/5/results", views.results, name="results"),
    path("/fitnessTrackerApp/5/vote/", views.vote, name="vote"),

    # URLs for catalog features
    path('workouts/', views.workout_catalog, name='workout_catalog'),
    path('workouts/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('diets/', views.diet_catalog, name='diet_catalog'),
    path('diets/<int:diet_id>/', views.diet_detail, name='diet_detail'),

]