from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateAccountForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render
from .models import UserProfile
from .models import WorkoutPlan, DietPlan
from django.contrib.auth.password_validation import validate_password


@login_required(login_url='/')
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'fitnessTrackerApp/profile.html', {'profile': profile})

@login_required(login_url='/')
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        goal = request.POST.get('goal')
        activity_level = request.POST.get('activity_level')


        try:
            weight = float(weight)
            height = float(height)
            age = int(age)

            if weight <= 0:
                messages.error(request, "Invalid weight")
            elif height <= 0:
                messages.error(request, "Invalid height")
            elif age <= 0:
                messages.error(request, "Invalid age")
            elif gender not in ['male', 'female', 'nonbinary']:
                messages.error(request, "Invalid gender")
            else:
                profile.weight = weight
                profile.height = height
                profile.age = age
                profile.gender = gender
                profile.goal = goal
                profile.activity_level = activity_level
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile_view')

        except ValueError:
            messages.error(request, "Please enter valid numeric values.")

    return render(request, 'fitnessTrackerApp/edit_profile.html', {'profile': profile})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'fitnessTrackerApp/home.html')  # back to login page!
    else:
        account_created = request.GET.get('account_created') == '1'
        return render(request, 'fitnessTrackerApp/home.html', {
            'account_created': account_created
        })

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'fitnessTrackerApp/home.html')

def index(request):
    return HttpResponse("Hello, world. You're at the default page.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



# views for workout and diet catalogs
def workout_catalog(request):
    workouts = WorkoutPlan.objects.all().order_by('difficulty_level', 'name')
    context = {
        'workouts': workouts,
        'title': 'Browse Workout Plans'
    }
    return render(request, 'fitnessTrackerApp/workout_catalog.html', context)

def workout_detail(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, pk=workout_id)
    exercises = workout.exercises.all().order_by('order')
    context = {
        'workout': workout,
        'exercises': exercises,
        'title': workout.name
    }
    return render(request, 'fitnessTrackerApp/workout_detail.html', context)

def diet_catalog(request):
    diets = DietPlan.objects.all().order_by('category', 'name')
    context = {
        'diets': diets,
        'title': 'Browse Diet Plans'
    }
    return render(request, 'fitnessTrackerApp/diet_catalog.html', context)

def diet_detail(request, diet_id):
    diet = get_object_or_404(DietPlan, pk=diet_id)
    meals = diet.meals.all()
    context = {
        'diet': diet,
        'meals': meals,
        'title': diet.name
    }
    return render(request, 'fitnessTrackerApp/diet_detail.html', context)

def guest_home(request):
    return render(request, 'fitnessTrackerApp/guest_home.html')

def guest_workouts(request):
    return render(request, 'fitnessTrackerApp/guest_workouts.html')

def guest_nutrition(request):
    return render(request, 'fitnessTrackerApp/guest_nutrition.html')

def guest_workout_fullbody(request):
    return render(request, 'fitnessTrackerApp/guest_workout_fullbody.html')
def guest_workout_hiit(request):
    return render(request, 'fitnessTrackerApp/guest_workout_hiit.html')
def guest_workout_strength(request):
    return render(request, 'fitnessTrackerApp/guest_workout_strength.html')
def guest_nutrition_balanced(request):
    return render(request, 'fitnessTrackerApp/guest_nutrition_balanced.html')
def guest_nutrition_protein(request):
    return render(request, 'fitnessTrackerApp/guest_nutrition_protein.html')
def guest_nutrition_lowcarb(request):
    return render(request, 'fitnessTrackerApp/guest_nutrition_lowcarb.html')
def guest_workout_ul(request):
    return render(request, 'fitnessTrackerApp/guest_workout_ul.html')
def guest_workout_ppl(request):
    return render(request, 'fitnessTrackerApp/guest_workout_ppl.html')
def user_workouts(request):
    return render(request, 'fitnessTrackerApp/user_workouts.html')

def user_nutrition(request):
    return render(request, 'fitnessTrackerApp/user_nutrition.html')

def user_workout_fullbody(request):
    return render(request, 'fitnessTrackerApp/user_workout_fullbody.html')
def user_workout_hiit(request):
    return render(request, 'fitnessTrackerApp/user_workout_hiit.html')
def user_workout_strength(request):
    return render(request, 'fitnessTrackerApp/user_workout_strength.html')
def user_nutrition_balanced(request):
    return render(request, 'fitnessTrackerApp/user_nutrition_balanced.html')
def user_nutrition_protein(request):
    return render(request, 'fitnessTrackerApp/user_nutrition_protein.html')
def user_nutrition_lowcarb(request):
    return render(request, 'fitnessTrackerApp/user_nutrition_lowcarb.html')
def user_workout_ul(request):
    return render(request, 'fitnessTrackerApp/user_workout_ul.html')
def user_workout_ppl(request):
    return render(request, 'fitnessTrackerApp/user_workout_ppl.html')

def ai_coach(request):
    return render(request, 'fitnessTrackerApp/ai_coach.html')
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(username) < 4:
            messages.error(request, 'Username too short. Must be at least 4 characters.')
            return redirect('create_account')

        # Match check first
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('create_account')

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('create_account')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email.')
            return redirect('create_account')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('create_account')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use another email.')
            return redirect('create_account')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('/?account_created=1')

    return render(request, 'fitnessTrackerApp/create_account.html')


@login_required(login_url='/')  # Redirects to login page if user is not logged in
def dashboard(request):
    return render(request, 'fitnessTrackerApp/dashboard.html')



