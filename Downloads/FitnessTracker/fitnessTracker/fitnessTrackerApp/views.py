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
from django.template.loader import render_to_string
from .models import WorkoutPlan, DietPlan
from django.contrib.auth.password_validation import validate_password
import google.generativeai as genai
import os # Good practice, though key is hardcoded below for this example


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
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'fitnessTrackerApp/home.html')
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

def call_ai_service(profile_data):
    # ---!!! VERY IMPORTANT SECURITY WARNING !!!---
    # --- Do NOT leave the API key hardcoded here in a real application ---
    # --- Use environment variables or Django settings instead ---
    api_key = "AIzaSyBknUlino8NHqQd5CcPoCBSAT65jJXmKpQ" # YOUR KEY HERE - REMOVE BEFORE PRODUCTION
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""You are a helpful AI fitness coach. Generate a personalized workout and nutrition plan for a user with the following details:

- Weight: {profile_data.get('weight', 'Not provided')} lbs
- Height: {profile_data.get('height', 'Not provided')} cm
- Age: {profile_data.get('age', 'Not provided')}
- Gender: {profile_data.get('gender', 'Not provided')}
- Fitness Goal: {profile_data.get('goal', 'Not specified')}
- Activity Level: {profile_data.get('activity_level', 'Not specified')}

Please provide a concise weekly workout plan suitable for their goal and activity level. 
Also provide a sample daily nutrition plan (ideas for breakfast, lunch, dinner, snacks) aligned with their goal.
Structure the response clearly, starting the workout plan section with the heading '### Workout Plan' on its own line, 
and starting the nutrition plan section with the heading '### Nutrition Plan' on its own line.
Keep the descriptions relatively brief and easy to follow. Format the output using Markdown.
"""

        response = model.generate_content(prompt)
        full_response_text = response.text

        workout_plan_text = "Could not parse workout plan from AI response."
        nutrition_plan_text = "Could not parse nutrition plan from AI response."

        # Try to split the response based on the headings
        nutrition_heading = "### Nutrition Plan"
        workout_heading = "### Workout Plan"

        if nutrition_heading in full_response_text:
            parts = full_response_text.split(nutrition_heading, 1)
            potential_workout = parts[0]
            nutrition_plan_text = parts[1].strip()
            if workout_heading in potential_workout:
                 workout_plan_text = potential_workout.split(workout_heading, 1)[1].strip()
            else:
                 # If workout heading not found before nutrition, maybe it was the whole first part?
                 workout_plan_text = potential_workout.strip()
        elif workout_heading in full_response_text:
             # Only workout found
             workout_plan_text = full_response_text.split(workout_heading, 1)[1].strip()
             nutrition_plan_text = "Nutrition plan not found in response."
        else:
             # Neither heading found, return the whole text as workout? Or indicate error?
             workout_plan_text = full_response_text # Assign the whole response to workout as a fallback
             nutrition_plan_text = "Could not find specific nutrition section."


        return workout_plan_text, nutrition_plan_text

    except Exception as e:
        print(f"Error calling Google AI: {e}")
        error_message = f"Error communicating with AI. Please check configuration. Details: {e}"
        return error_message, error_message


@login_required(login_url='/')
def ai_coach(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    generated_workout = None
    generated_nutrition = None

    if request.method == 'POST':
        print(f"AI Coach generation requested by: {request.user.username}")

        if not profile.weight or not profile.height or not profile.age or not profile.gender or not profile.goal or not profile.activity_level:
             messages.warning(request, "Please complete your profile before generating a plan!")
        else:
            profile_data = {
                'weight': profile.weight,
                'height': profile.height,
                'age': profile.age,
                'gender': profile.gender,
                'goal': profile.goal,
                'activity_level': profile.activity_level,
            }
            try:
                generated_workout, generated_nutrition = call_ai_service(profile_data)
                messages.success(request, "Your personalized plan has been generated below!")
            except Exception as e:
                messages.error(request, f"Sorry, there was an error generating the plan: {e}")
                print(f"Error in AI generation process: {e}")

    context = {
         'profile': profile,
         'generated_workout': generated_workout,
         'generated_nutrition': generated_nutrition,
    }
    return render(request, 'fitnessTrackerApp/ai_coach.html', context)


def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(username) < 4:
            messages.error(request, 'Username too short. Must be at least 4 characters.')
            return redirect('create_account')

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


@login_required(login_url='/')
def dashboard(request):
    return render(request, 'fitnessTrackerApp/dashboard.html')