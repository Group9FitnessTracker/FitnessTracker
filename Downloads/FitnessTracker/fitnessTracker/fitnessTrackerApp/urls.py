from django.urls import path
from django.contrib.auth import views as auth_views
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

    path('guest_home/', views.guest_home, name='guest_home'),
    path('guest_workouts/', views.guest_workouts, name='guest_workouts'),
    path('guest_nutrition/', views.guest_nutrition, name='guest_nutrition'),
    path('guest_workout_fullbody/', views.guest_workout_fullbody, name='guest_workout_fullbody'),
    path('guest_workout_hiit/', views.guest_workout_hiit, name='guest_workout_hiit'),
    path('guest_workout_strength/', views.guest_workout_strength, name='guest_workout_strength'),
    path('guest_nutrition_balanced/', views.guest_nutrition_balanced, name='guest_nutrition_balanced'),
    path('guest_nutrition_protein/', views.guest_nutrition_protein, name='guest_nutrition_protein'),
    path('guest_nutrition_lowcarb/', views.guest_nutrition_lowcarb, name='guest_nutrition_lowcarb'),
    path('guest_workout_ul/', views.guest_workout_ul, name='guest_workout_ul'),
    path('guest_workout_ppl/', views.guest_workout_ppl, name='guest_workout_ppl'),
    path('ai_coach/', views.ai_coach, name='ai_coach'),
    path('create_account/', views.create_account, name='create_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="fitnessTrackerApp/password_reset_sent.html"), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="fitnessTrackerApp/password_reset_confirm.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="fitnessTrackerApp/password_reset_complete.html"), 
         name="password_reset_complete"),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(
         template_name='fitnessTrackerApp/password_reset.html',
         email_template_name='registration/password_reset_email.html',
         subject_template_name='registration/password_reset_subject.txt'
     ),
     name='reset_password'),




]