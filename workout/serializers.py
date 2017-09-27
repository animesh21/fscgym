from rest_framework import serializers
from django.contrib.auth.models import User
from . import models  # import Story, Day, Slot, GymSession, Category, Exercise


# Signup and login stuff
class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', '')
        if instance.check_password(password):
            instance.set_password(password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'email', 'is_staff')


class UserCreateSerializer(serializers.ModelSerializer):

    pk = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username',
                  'email', 'password')


# Home page and feed stuff
class StorySerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='workout:story-detail',
        lookup_field='pk'
    )

    class Meta:
        model = models.Story
        fields = ('pk', 'url', 'title', 'subtitle', 'image')


class StoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Story
        fields = ('pk', 'title', 'subtitle', 'text', 'image', 'created')


# Booking stuff
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('pk', 'name')


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slot
        fields = ('pk', 'start_time')


class GymSessionSerializer(serializers.ModelSerializer):

    num_slots_available = serializers.IntegerField()

    is_slot_available = serializers.BooleanField()

    class Meta:
        model = models.GymSession
        fields = ('pk', 'date', 'day', 'slot', 'capacity',
                  'num_slots_available', 'is_slot_available', 'users_registered')


# Workout category and exercise stuff
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('pk', 'name', 'description', 'image')


class ExerciseSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Exercise
        fields = ('pk', 'category', 'name', 'description', 'image')


# User workout, exercise and timer stuff
class GymCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GymCategory
        fields = ('pk', 'name', 'image')


class GymExerciseSerializer(serializers.ModelSerializer):

    gym_category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.GymExercise
        fields = ('pk', 'name', 'image', 'gym_category', 'default_timeout')


class WorkoutSerializer(serializers.ModelSerializer):

    gym_exercise_name = serializers.StringRelatedField(
        source='gym_exercise', read_only=True)

    class Meta:
        model = models.Workout
        fields = ('pk', 'user', 'gym_exercise', 'gym_exercise_name',
                  'timeout', 'sets', 'reps')


class DailyWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyWeight
        fields = ('pk', 'user', 'weight', 'date')
