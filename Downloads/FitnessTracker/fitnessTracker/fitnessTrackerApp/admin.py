from django.contrib import admin

from .models import Question, WorkoutPlan, WorkoutExercise, DietPlan, Meal, UserProfile, UserWorkoutPlan, UserDietPlan

admin.site.register(Question)
admin.site.register(UserProfile)

#sites workout and diet catalogs
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutExercise)
admin.site.register(DietPlan)
admin.site.register(Meal)


#user saved plans
admin.site.register(UserWorkoutPlan)
admin.site.register(UserDietPlan)