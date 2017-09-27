from django.db import models
from django.contrib.auth.models import User
from datetime import time


class Story(models.Model):
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='uploads/stories/', blank=True)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = 'stories'
        ordering = ('-created', )

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=127)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/categories/', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/exercises/', blank=True)

    def __str__(self):
        return self.name


class Slot(models.Model):

    SLOT_1 = time(hour=6, minute=0, second=0)
    SLOT_2 = time(hour=6, minute=30, second=0)
    SLOT_3 = time(hour=17, minute=30, second=0)
    SLOT_4 = time(hour=18, minute=0, second=0)
    SLOT_5 = time(hour=9, minute=0, second=0)

    START_TIME_CHOICES = (
        (SLOT_1, SLOT_1.strftime('%I:%M %p')),
        (SLOT_2, SLOT_2.strftime('%I:%M %p')),
        (SLOT_3, SLOT_3.strftime('%I:%M %p')),
        (SLOT_4, SLOT_4.strftime('%I:%M %p')),
        (SLOT_5, SLOT_5.strftime('%I:%M %p')),
    )
    start_time = models.TimeField(choices=START_TIME_CHOICES, unique=True)

    class Meta:
        ordering = ('start_time', )

    def __str__(self):
        return self.start_time.strftime('%I:%M %p')


class Day(models.Model):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"

    DAY_NAME_CHOICES = (
        (SUNDAY, "Sunday"),
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
    )

    name = models.CharField(
        max_length=15,
        choices=DAY_NAME_CHOICES,
        unique=True
    )
    slots = models.ManyToManyField(Slot)

    def __str__(self):
        return self.name


class GymSession(models.Model):
    date = models.DateField()
    day = models.ForeignKey(Day, unique_for_date='date')
    slot = models.ForeignKey(Slot, unique_for_date='date')
    capacity = models.IntegerField(default=15)
    users_registered = models.ManyToManyField(
        User, related_name='sessions_registered', blank=True
    )
    users_attended = models.ManyToManyField(
        User, related_name='sessions_attended', blank=True
    )

    def num_slots_available(self):
        return self.capacity - self.users_registered.count()

    def is_slot_available(self):
        return self.num_slots_available() > 0

    def __str__(self):
        return '{}: {}'.format(self.day.name, self.slot.start_time)


class GymCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/gym_categories/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'gym categories'


class GymExercise(models.Model):
    name = models.CharField(max_length=63)
    image = models.ImageField(upload_to='uploads/gym_exercises/', blank=True)
    gym_category = models.ForeignKey(GymCategory)
    default_timeout = models.DurationField(blank=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User)
    gym_exercise = models.ForeignKey(GymExercise)
    timeout = models.DurationField(blank=True)
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.gym_exercise.name)


class DailyWeight(models.Model):
    user = models.ForeignKey(User, unique_for_date='date')
    weight = models.FloatField(null=True, help_text='Weight in kg')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.weight)

    class Meta:
        ordering = ('-date', )
