from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateAccountForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserProfile

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
        return render(request, 'fitnessTrackerApp/home.html')



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

def ai_coach(request):
    return render(request, 'fitnessTrackerApp/ai_coach.html')
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        # Username length check
        if len(username) < 4:
            messages.error(request, 'Username too short. Must be at least 4 characters.')
            return redirect('create_account')

        # Password strength check
        if len(password) < 6:
            messages.error(request, 'Password too weak. Must be at least 6 characters.')
            return redirect('create_account')

        # Password match check
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('create_account')

        # Phone number: clean non-digit characters
        cleaned_phone = re.sub(r'\D', '', phone_number)
        if not re.fullmatch(r'\d{10,15}', cleaned_phone):
            messages.error(request, 'Invalid phone number. Must be 10-15 digits after removing dashes and spaces.')
            return redirect('create_account')

        # Email validity check
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email.')
            return redirect('create_account')

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('create_account')

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use another email.')
            return redirect('create_account')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Optionally you could save cleaned_phone into a future profile model here

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('/')

    return render(request, 'fitnessTrackerApp/create_account.html')


@login_required(login_url='/')  # Redirects to login page if user is not logged in
def dashboard(request):
    return render(request, 'fitnessTrackerApp/dashboard.html')



