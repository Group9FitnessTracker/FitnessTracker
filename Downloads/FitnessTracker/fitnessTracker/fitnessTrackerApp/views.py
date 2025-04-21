from django.http import HttpResponse
from django.shortcuts import render

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


