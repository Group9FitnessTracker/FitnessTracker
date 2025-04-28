from django.contrib import admin

from .models import Question, WorkoutPlan, WorkoutExercise, DietPlan, Meal

admin.site.register(Question)

#sites workout and diet catalogs
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutExercise)
admin.site.register(DietPlan)
admin.site.register(Meal)