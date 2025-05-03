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
from django.db import IntegrityError
from .models import (
    UserProfile, WorkoutPlan, DietPlan, 
    UserWorkoutPlan, UserDietPlan
)


@login_required(login_url='/')
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    saved_workouts = UserWorkoutPlan.objects.filter(user=request.user).select_related('workout_plan')
    saved_diets = UserDietPlan.objects.filter(user=request.user).select_related('diet_plan')
    
    context = {
        'profile': profile,
        'saved_workouts': saved_workouts,
        'saved_diets': saved_diets
    }
    return render(request, 'fitnessTrackerApp/profile.html', context)

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



# Views for workout and diet catalogs
def workout_catalog(request):
    workouts = WorkoutPlan.objects.all().order_by('difficulty_level', 'name')
    
    # cChecks the workout plans that a user has 
    user_saved_workout_ids = []
    if request.user.is_authenticated:
        user_saved_workout_ids = UserWorkoutPlan.objects.filter(
            user=request.user
        ).values_list('workout_plan_id', flat=True)
    
    context = {
        'workouts': workouts,
        'title': 'Browse Workout Plans',
        'user_saved_workout_ids': user_saved_workout_ids
    }
    return render(request, 'fitnessTrackerApp/workout_catalog.html', context)

def workout_detail(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, pk=workout_id)
    exercises = workout.exercises.all().order_by('order')
    
    # Makes sure user has workout plans 
    is_saved = False
    if request.user.is_authenticated:
        is_saved = UserWorkoutPlan.objects.filter(
            user=request.user, 
            workout_plan=workout
        ).exists()
    
    context = {
        'workout': workout,
        'exercises': exercises,
        'title': workout.name,
        'is_saved': is_saved
    }
    return render(request, 'fitnessTrackerApp/workout_detail.html', context)

@login_required(login_url='/')
def save_workout(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, pk=workout_id)
    notes = request.POST.get('notes', '')
    
    # Makes sure user does not add the same workout plan
    try:
        # Make plans a part of a user
        UserWorkoutPlan.objects.create(
            user=request.user,
            workout_plan=workout,
            notes=notes
        )
        messages.success(request, f"'{workout.name}' has been saved to your account!")
    except IntegrityError:
        messages.info(request, "You've already saved this workout plan.")
    
    return redirect('workout_detail', workout_id=workout_id)

@login_required(login_url='/')
def remove_workout(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, pk=workout_id)
    
    UserWorkoutPlan.objects.filter(
        user=request.user,
        workout_plan=workout
    ).delete()
    
    messages.success(request, f"'{workout.name}' has been removed from your saved workouts.")
    
    next_page = request.GET.get('next', 'profile_view')
    if next_page == 'detail':
        return redirect('workout_detail', workout_id=workout_id)
    return redirect('profile_view')

def diet_catalog(request):
    diets = DietPlan.objects.all().order_by('category', 'name')
    
    # Checks the diet plans that a user has 
    user_saved_diet_ids = []
    if request.user.is_authenticated:
        user_saved_diet_ids = UserDietPlan.objects.filter(
            user=request.user
        ).values_list('diet_plan_id', flat=True)
    
    context = {
        'diets': diets,
        'title': 'Browse Diet Plans',
        'user_saved_diet_ids': user_saved_diet_ids
    }
    return render(request, 'fitnessTrackerApp/diet_catalog.html', context)

def diet_detail(request, diet_id):
    diet = get_object_or_404(DietPlan, pk=diet_id)
    meals = diet.meals.all()
    
    # Makes sure user has diet plans 
    is_saved = False
    if request.user.is_authenticated:
        is_saved = UserDietPlan.objects.filter(
            user=request.user, 
            diet_plan=diet
        ).exists()
    
    context = {
        'diet': diet,
        'meals': meals,
        'title': diet.name,
        'is_saved': is_saved
    }
    return render(request, 'fitnessTrackerApp/diet_detail.html', context)

@login_required(login_url='/')
def save_diet(request, diet_id):
    diet = get_object_or_404(DietPlan, pk=diet_id)
    notes = request.POST.get('notes', '')
    
    # Makes sure user does not add the same workout plan
    try:
        # Make plans a part of a user
        UserDietPlan.objects.create(
            user=request.user,
            diet_plan=diet,
            notes=notes
        )
        messages.success(request, f"'{diet.name}' has been saved to your account!")
    except IntegrityError:
        messages.info(request, "You've already saved this diet plan.")
    
    return redirect('diet_detail', diet_id=diet_id)

@login_required(login_url='/')
def remove_diet(request, diet_id):
    diet = get_object_or_404(DietPlan, pk=diet_id)
    
    UserDietPlan.objects.filter(
        user=request.user,
        diet_plan=diet
    ).delete()
    
    messages.success(request, f"'{diet.name}' has been removed from your saved diets.")
    
    next_page = request.GET.get('next', 'profile_view')
    if next_page == 'detail':
        return redirect('diet_detail', diet_id=diet_id)
    return redirect('profile_view')

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

        # Create a user profile
        UserProfile.objects.create(user=user)

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('/')

    return render(request, 'fitnessTrackerApp/create_account.html')


@login_required(login_url='/')  # Redirects to login page if user is not logged in
def dashboard(request):
    saved_workouts = UserWorkoutPlan.objects.filter(user=request.user).select_related('workout_plan')
    saved_diets = UserDietPlan.objects.filter(user=request.user).select_related('diet_plan')
    
    context = {
        'saved_workouts': saved_workouts,
        'saved_diets': saved_diets
    }
    return render(request, 'fitnessTrackerApp/dashboard.html', context)


@login_required(login_url='/')
def add_plans(request):
    """
    View function for the add plans page that displays available workout
    and diet plans for users to save to their account.
    """
    workouts = WorkoutPlan.objects.all().order_by('difficulty_level', 'name')
    diets = DietPlan.objects.all().order_by('category', 'name')
    
    user_saved_workout_ids = UserWorkoutPlan.objects.filter(
        user=request.user
    ).values_list('workout_plan_id', flat=True)
    
    user_saved_diet_ids = UserDietPlan.objects.filter(
        user=request.user
    ).values_list('diet_plan_id', flat=True)
    
    context = {
        'workouts': workouts,
        'diets': diets,
        'user_saved_workout_ids': user_saved_workout_ids,
        'user_saved_diet_ids': user_saved_diet_ids,
        'title': 'Add Plans'
    }
    
    return render(request, 'fitnessTrackerApp/add_plans.html', context)

@login_required(login_url='/')
def saved_plans(request):
    saved_workouts = UserWorkoutPlan.objects.filter(user=request.user).select_related('workout_plan')
    saved_diets = UserDietPlan.objects.filter(user=request.user).select_related('diet_plan')
    
    context = {
        'saved_workouts': saved_workouts,
        'saved_diets': saved_diets,
        'title': 'Saved Plans'
    }
    return render(request, 'fitnessTrackerApp/saved_plans.html', context)