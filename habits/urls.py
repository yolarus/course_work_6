from django.urls import path

from . import views
from .apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("habits/", views.HabitListCreateAPIView.as_view(), name="habits"),
    path("habits/public/", views.HabitListPublicAPIView.as_view(), name="habits-public"),
    path("habits/<int:pk>/", views.HabitRetrieveUpdateDestroyAPIView.as_view(), name="habit"),

    path("places/", views.PlaceListCreateAPIView.as_view(), name="places"),
    path("places/<int:pk>/", views.PlaceRetrieveUpdateDestroyAPIView.as_view(), name="place"),
]
