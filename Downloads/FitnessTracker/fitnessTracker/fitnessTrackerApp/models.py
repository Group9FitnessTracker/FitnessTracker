import datetime
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('nonbinary', 'Non-binary')
    ], null=True, blank=True)
    goal = models.CharField(max_length=100, null=True, blank=True)
    activity_level = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
# models for workout and diet catalogs
class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    duration_minutes = models.IntegerField()
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

    
class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    sets = models.IntegerField()
    reps = models.CharField(max_length=50) 
    rest_seconds = models.IntegerField()
    order = models.IntegerField()  
    
    def __str__(self):
        return f"{self.name} ({self.workout_plan.name})"


class DietPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calorie_target = models.IntegerField()
    category = models.CharField(max_length=50)  
    
    def __str__(self):
        return self.name


class Meal(models.Model):
    diet_plan = models.ForeignKey(DietPlan, related_name='meals', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    description = models.TextField()
    calorie_count = models.IntegerField()
    protein_grams = models.IntegerField()
    carbs_grams = models.IntegerField()
    fat_grams = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.diet_plan.name})"