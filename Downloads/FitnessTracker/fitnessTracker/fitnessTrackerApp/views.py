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

from django.utils import timezone

from django.db import IntegrityError
from .models import (
    UserProfile, WorkoutPlan, DietPlan, 
    UserWorkoutPlan, UserDietPlan, UserCustomWorkoutPlan, UserCustomDietPlan
)


from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.password_validation import validate_password
import google.generativeai as genai
import os # Good practice, though key is hardcoded below for this example



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
         'current_date': timezone.now().strftime("%Y-%m-%d"),
    }
    return render(request, 'fitnessTrackerApp/ai_coach.html', context)


@login_required(login_url='/')
def save_ai_plans(request):
    if request.method == "POST":
        title_prefix = request.POST.get("title_prefix", "AI Plan")
        workout_content = request.POST.get("workout_content")
        diet_content = request.POST.get("diet_content")
        current_date = request.POST.get("current_date")
        
        # Format the content to display properly in HTML
        formatted_workout_content = workout_content.replace('\n', '<br>') if workout_content else None
        formatted_diet_content = diet_content.replace('\n', '<br>') if diet_content else None
        
        # Save workout plan if it exists
        if formatted_workout_content:
            UserCustomWorkoutPlan.objects.create(
                user=request.user,
                title=f"{title_prefix} - Workout - {current_date}",
                content=formatted_workout_content
            )
        
        # Save diet plan if it exists
        if formatted_diet_content:
            UserCustomDietPlan.objects.create(
                user=request.user,
                title=f"{title_prefix} - Diet - {current_date}",
                content=formatted_diet_content
            )
        
        messages.success(request, "AI Plans saved successfully!")
        return redirect('ai_coach')
    return redirect('ai_coach')


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


        # Create a user profile (mark)
        UserProfile.objects.create(user=user)

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('/')
   #(end of mark)
        #return redirect('/?account_created=1')


    return render(request, 'fitnessTrackerApp/create_account.html')


@login_required(login_url='/')
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
    
    return render(request, 'fitnessTrackerApp/saved_plans.html', context)

@login_required(login_url='/')
def saved_plans(request):
    saved_workouts = UserWorkoutPlan.objects.filter(user=request.user).select_related('workout_plan')
    saved_diets = UserDietPlan.objects.filter(user=request.user).select_related('diet_plan')
    custom_saved_workouts = UserCustomWorkoutPlan.objects.filter(user=request.user)
    custom_saved_diets = UserCustomDietPlan.objects.filter(user=request.user)
    context = {
        'saved_workouts': saved_workouts,
        'saved_diets': saved_diets,
        'custom_saved_workouts': custom_saved_workouts,
        'custom_saved_diets': custom_saved_diets,
        'title': 'Saved Plans'
    }
    return render(request, 'fitnessTrackerApp/saved_plans.html', context)

   # return render(request, 'fitnessTrackerApp/dashboard.html')

@login_required(login_url='/')
def save_custom_workout(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        UserCustomWorkoutPlan.objects.create(user=request.user, title=title, content=content)
    return redirect('user_workout_ul')

@login_required(login_url='/')
def save_custom_diet(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        UserCustomDietPlan.objects.create(user=request.user, title=title, content=content)
    return redirect('user_nutrition')


@login_required(login_url='/')
def remove_custom_workout(request, workout_id):
    """
    View function to remove a custom workout plan
    """
    workout = get_object_or_404(UserCustomWorkoutPlan, pk=workout_id, user=request.user)
    workout_title = workout.title
    workout.delete()
    
    messages.success(request, f"'{workout_title}' has been removed from your saved workouts.")
    return redirect('saved_plans')

@login_required(login_url='/')
def remove_custom_diet(request, diet_id):
    """
    View function to remove a custom diet plan
    """
    diet = get_object_or_404(UserCustomDietPlan, pk=diet_id, user=request.user)
    diet_title = diet.title
    diet.delete()
    
    messages.success(request, f"'{diet_title}' has been removed from your saved diets.")
    return redirect('saved_plans')