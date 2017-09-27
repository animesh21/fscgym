from django.contrib import admin
from . import models


admin.site.register(
    (models.Story, models.Category, models.Exercise, models.Day,
     models.Slot, models.GymSession, models.GymCategory, models.GymExercise,
     models.Workout, models.DailyWeight)
)
