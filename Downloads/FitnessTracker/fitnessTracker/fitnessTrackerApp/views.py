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
from huggingface_hub import InferenceClient
from django.conf import settings
import requests


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

def ai_question(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        experience = request.POST.get('experience')
        preferences = request.POST.get('preferences')

        if goal and experience and preferences:
            request.session['goal'] = goal
            request.session['experience'] = experience
            request.session['preferences'] = preferences
            return redirect('ai_recommendation')  # This is the key line
    return render(request, 'fitnessTrackerApp/ai_question.html')

def ai_recommendation(request):
    # Get user inputs from session
    goal = request.session.get('goal', '')
    experience = request.session.get('experience', '')
    preferences = request.session.get('preferences', '')

    # Redirect if any input is missing
    if not (goal and experience and preferences):
        return redirect('ai_question')

    # Create prompt for Gemini
    prompt = (
    f"Create a 7-day personalized fitness plan for someone with the goal: {goal}, "
    f"experience level: {experience}, and preferences: {preferences}. "
    "Each day should include:\n"
    "- 3 distinct workout sessions (e.g., morning, afternoon, evening)\n"
    "- 3 unique meals (breakfast, lunch, dinner), different from other days\n\n"
    "Format each day like this:\n"
    "Workouts:\n"
    "- Morning: ...\n"
    "- Afternoon: ...\n"
    "- Evening: ...\n"
    "Meals:\n"
    "- Breakfast: ...\n"
    "- Lunch: ...\n"
    "- Dinner: ...\n"
    "###ENDDAY###\n\n"
    "Repeat for 7 days, using ###ENDDAY### after each day's content. Do not include any introductory paragraph or 'Day X' labels."
)



    generated_plan = ""
    error_message = ""
    days = []

    try:
        # Send prompt to Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extract generated text
        generated_plan = result['candidates'][0]['content']['parts'][0]['text'].strip()
        days = [d.strip() for d in generated_plan.split("###ENDDAY###") if d.strip()]
        days = [f"Day {i + 1}\n\n{d}" for i, d in enumerate(days)]



    except Exception as e:
        error_message = f"There was an error: {str(e)}"
        days = [generated_plan] if generated_plan else []

    # Render page
    context = {
        'days': days,
        'user_goal': goal,
        'user_experience': experience,
        'user_preferences': preferences,
        'error_occurred': bool(error_message),
        'error_details': error_message
    }

    return render(request, 'fitnessTrackerApp/ai_recommendation.html', context)

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



