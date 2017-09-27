from rest_framework import permissions, status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils.timezone import datetime, timedelta
from .response import StandardResponse
from . import serializers
from . import models


class SignupView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        # username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        username = email
        if first_name and last_name and username:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email)
            user.set_password(password)
            user.save()
            user_serializer = serializers.UserSerializer(instance=user)
            data = user_serializer.data
            message = 'user created successfully'
            status_code = status.HTTP_201_CREATED
        else:
            data = {'data': 'insufficient information'}
            message = 'insufficient information provided'
            status_code = status.HTTP_400_BAD_REQUEST
        return StandardResponse(
            status=status_code,
            message=message,
            data=data)


class LoginView(APIView):

    http_method_names = ['post', ]

    def post(self, request):
        data = request.data
        try:
            credentials = dict(username=data['username'], password=data['password'])
        except KeyError as e:
            data = {'message': 'username or password not present in the data.',
                    'error': e}
            return StandardResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message='credentials not provided',
                data=data)
        user = authenticate(**credentials)
        if user:
            login(request, user)
            user_serializer = serializers.UserSerializer(user, context={'request': request})
            return StandardResponse(status=status.HTTP_200_OK,
                                    message='login successful',
                                    data=user_serializer.data)
        else:
            return StandardResponse(status=status.HTTP_401_UNAUTHORIZED,
                                    message='invalid credentials',
                                    data={'user': 'anonymous user'})


class LogoutView(APIView):

    http_method_names = ['get', ]

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        if request.user is not None:
            logout(request)
            return Response(data={'message': 'logout successful!'},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'message': 'user was not logged in'},
                            status=status.HTTP_400_BAD_REQUEST)


class StoryList(generics.ListAPIView):
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class StoryDetail(generics.RetrieveAPIView):
    queryset = models.Story.objects.all()
    serializer_class = serializers.StoryDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DayList(generics.ListAPIView):
    queryset = models.Day.objects.all()
    serializer_class = serializers.DaySerializer
    permission_classes = (permissions.AllowAny, )


class SlotList(generics.ListAPIView):
    serializer_class = serializers.SlotSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        pk = self.kwargs['day_pk']
        day = get_object_or_404(models.Day, pk=pk)
        return day.slots.all()


def get_date_from_day(day):
    for i in range(7):
        datetime_then = datetime.now() + timedelta(days=i)
        date = datetime_then.date()
        if date.strftime("%A") == day:
            return date


class GymSessionViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        try:
            day_pk = int(data.get('day'))
            slot_pk = int(data.get('slot'))
            user_pk = int(data.get('user'))
        except (ValueError, TypeError) as e:
            raise ValidationError('Invalid Value provided for day, slot'
                                  ' or user: ' + str(e))
        day = get_object_or_404(models.Day, pk=day_pk)
        date = get_date_from_day(day.name)
        slot = get_object_or_404(models.Slot, pk=slot_pk)
        user = get_object_or_404(User, pk=user_pk)
        gym_session, _ = models.GymSession.objects.get_or_create(
            date=date, day=day, slot=slot
        )

        if gym_session.users_registered.filter(id=user_pk).exists():
            serializer = serializers.GymSessionSerializer(gym_session)
            serialized_data = serializer.data
            serialized_data['message'] = 'You have already registered for this session'
            return Response(serialized_data, status=status.HTTP_406_NOT_ACCEPTABLE)

        if gym_session.is_slot_available():
            gym_session.users_registered.add(user)
            serializer = serializers.GymSessionSerializer(gym_session)
            return Response(serializer.data)
        else:
            raise ValidationError('No slots available')

    def get(self, request):
        serializer = serializers.GymSessionSerializer(
            models.GymSession.objects.all(), many=True
        )
        return Response(data=serializer.data)


class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny, )


class ExerciseList(generics.ListAPIView):
    serializer_class = serializers.ExerciseSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        pk = self.kwargs['cat_pk']
        category = get_object_or_404(models.Category, pk=pk)
        return category.exercise_set.all()


class GymCategoryList(generics.ListAPIView):
    queryset = models.GymCategory.objects.all()
    serializer_class = serializers.GymCategorySerializer
    permission_classes = (permissions.AllowAny, )


class GymExerciseList(generics.ListAPIView):
    serializer_class = serializers.GymExerciseSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        pk = self.kwargs['gym_cat_pk']
        gym_category = get_object_or_404(models.GymCategory, pk=pk)
        return gym_category.gymexercise_set.all()


class WorkoutView(generics.ListCreateAPIView):
    serializer_class = serializers.WorkoutSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        pk = self.kwargs.get('user', 0)
        try:
            pk = int(pk)
        except (ValueError, TypeError) as e:
            raise ValidationError('Not a valid value for user id: ' + str(e))
        user = get_object_or_404(User, pk=pk)
        return user.workout_set.all()


class DailyWeightView(generics.ListCreateAPIView):
    serializer_class = serializers.DailyWeightSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        pk = self.kwargs.get('user', 0)
        try:
            pk = int(pk)
        except (TypeError, ValueError) as e:
            raise ValidationError('Invalid user: ' + str(e))
        user = get_object_or_404(User, pk=pk)
        return user.dailyweight_set.all()

    def create(self, request, *args, **kwargs):
        date = datetime.now().date()

        data = request.data
        user_pk = data.get('user', 0)
        weight = data.get('weight', 0)

        user = get_object_or_404(User, pk=user_pk)
        daily_weight = models.DailyWeight.objects.get_or_create(
            user=user, date=date)[0]
        daily_weight.weight = weight
        daily_weight.save()
        serializer = serializers.DailyWeightSerializer(instance=daily_weight)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
