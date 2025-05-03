from django.core.management.base import BaseCommand
from fitnessTrackerApp.models import WorkoutPlan, WorkoutExercise, DietPlan, Meal

class Command(BaseCommand):
    help = 'Creates sample workout and diet plans for the fitness tracker app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample workout and diet plans...')
        
        WorkoutPlan.objects.all().delete()
        DietPlan.objects.all().delete()
        
        self.create_workout_plans()

        self.create_diet_plans()
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))
    
    def create_workout_plans(self):
        # 1. Beginner Full Body Workout
        fullbody = WorkoutPlan.objects.create(
            name="Beginner Full Body Workout",
            description="A complete full-body workout designed for beginners. This routine focuses on building strength and conditioning across all major muscle groups with basic exercises that are easy to learn and perform.",
            difficulty_level="beginner",
            duration_minutes=45,
            category="strength"
        )
        
        exercises = [
            {
                "name": "Bodyweight Squats",
                "description": "Stand with feet shoulder-width apart, lower your body by bending your knees as if sitting in a chair, then return to starting position.",
                "sets": 3,
                "reps": "12-15",
                "rest_seconds": 60,
                "order": 1
            },
            {
                "name": "Push-ups (or Modified Push-ups)",
                "description": "Start in a plank position with hands slightly wider than shoulders. Lower your body until chest nearly touches the floor, then push back up. For modified version, keep knees on the ground.",
                "sets": 3,
                "reps": "8-12",
                "rest_seconds": 60,
                "order": 2
            }
        ]
        
        for exercise in exercises:
            WorkoutExercise.objects.create(
                workout_plan=fullbody,
                name=exercise["name"],
                description=exercise["description"],
                sets=exercise["sets"],
                reps=exercise["reps"],
                rest_seconds=exercise["rest_seconds"],
                order=exercise["order"]
            )
        
        # 2. HIIT Cardio Workout
        hiit = WorkoutPlan.objects.create(
            name="HIIT Cardio Blast",
            description="High-Intensity Interval Training workout designed to boost cardiovascular fitness and burn calories. This workout alternates between intense bursts of activity and fixed periods of less-intense activity or rest.",
            difficulty_level="intermediate",
            duration_minutes=30,
            category="cardio"
        )
        
        # Add exercises to HIIT workout
        hiit_exercises = [
            {
                "name": "High Knees",
                "description": "Run in place, bringing knees up to waist level with each step while pumping arms.",
                "sets": 4,
                "reps": "30 seconds on, 15 seconds rest",
                "rest_seconds": 15,
                "order": 1
            },
            {
                "name": "Plank Jacks",
                "description": "Start in a plank position, jump feet out wide and then back together, similar to a jumping jack motion.",
                "sets": 4,
                "reps": "30 seconds on, 15 seconds rest",
                "rest_seconds": 15,
                "order": 2
            }
        ]
        
        for exercise in hiit_exercises:
            WorkoutExercise.objects.create(
                workout_plan=hiit,
                name=exercise["name"],
                description=exercise["description"],
                sets=exercise["sets"],
                reps=exercise["reps"],
                rest_seconds=exercise["rest_seconds"],
                order=exercise["order"]
            )
    
    def create_diet_plans(self):
        # 1. Balanced Nutrition Plan
        balanced = DietPlan.objects.create(
            name="Balanced Nutrition Plan",
            description="A well-rounded nutrition plan that provides a balance of all macronutrients. This plan focuses on whole foods, lean proteins, complex carbohydrates, and healthy fats to support overall health and fitness goals.",
            calorie_target=2000,
            category="balanced"
        )
        
        balanced_meals = [
            {
                "name": "Breakfast",
                "description": "Oatmeal with berries and a side of scrambled eggs.",
                "calorie_count": 400,
                "protein_grams": 20,
                "carbs_grams": 45,
                "fat_grams": 15
            },
            {
                "name": "Lunch",
                "description": "Grilled chicken salad with mixed vegetables and olive oil dressing.",
                "calorie_count": 450,
                "protein_grams": 35,
                "carbs_grams": 20,
                "fat_grams": 25
            }
        ]
        
        for meal in balanced_meals:
            Meal.objects.create(
                diet_plan=balanced,
                name=meal["name"],
                description=meal["description"],
                calorie_count=meal["calorie_count"],
                protein_grams=meal["protein_grams"],
                carbs_grams=meal["carbs_grams"],
                fat_grams=meal["fat_grams"]
            )
        
        # 2. High Protein Diet
        protein = DietPlan.objects.create(
            name="High Protein Diet",
            description="A nutrition plan focused on maximizing protein intake to support muscle growth and recovery. This plan includes lean protein sources with each meal while maintaining moderate carbohydrate and fat intake.",
            calorie_target=2200,
            category="protein"
        )
        
        protein_meals = [
            {
                "name": "Breakfast",
                "description": "Protein pancakes with Greek yogurt and berries.",
                "calorie_count": 450,
                "protein_grams": 40,
                "carbs_grams": 35,
                "fat_grams": 12
            },
            {
                "name": "Lunch",
                "description": "Tuna steak with quinoa and steamed vegetables.",
                "calorie_count": 500,
                "protein_grams": 45,
                "carbs_grams": 30,
                "fat_grams": 20
            }
        ]
        
        for meal in protein_meals:
            Meal.objects.create(
                diet_plan=protein,
                name=meal["name"],
                description=meal["description"],
                calorie_count=meal["calorie_count"],
                protein_grams=meal["protein_grams"],
                carbs_grams=meal["carbs_grams"],
                fat_grams=meal["fat_grams"]
            )