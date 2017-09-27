from workout import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^signup$', views.SignupView.as_view(), name='signup'),

    url(r'^login$', views.LoginView.as_view(), name='login'),

    url(r'^stories$', views.StoryList.as_view(), name='story-list'),

    url(r'^story/(?P<pk>[0-9]+)$', views.StoryDetail.as_view(),
        name="story-detail"),

    url(r'^days$', views.DayList.as_view(), name='day-list'),

    url(r'^slots/(?P<day_pk>[0-9]+)$', views.SlotList.as_view(),
        name='slot-list'),

    url(r'^book_slot$', views.GymSessionViewSet.as_view(
        {'post': 'post', 'get': 'get'}), name='book-slot'),

    url(r'^categories$', views.CategoryList.as_view(),
        name='category-list'),

    url(r'^exercises/(?P<cat_pk>[0-9]+)$', views.ExerciseList.as_view(),
        name='exercise-list'),

    url(r'^gym-categories$', views.GymCategoryList.as_view(),
        name='gym-category-list'),

    url(r'^gym-exercises/(?P<gym_cat_pk>[0-9]+)$',
        views.GymExerciseList.as_view(), name='gym-exercise-list'),

    url(r'^workout/(?P<user>[0-9]+)$', views.WorkoutView.as_view(), name='workout-list'),

    url(r'^daily-weight/(?P<user>[0-9]+)$', views.DailyWeightView.as_view(), name='daily-weight-list')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
