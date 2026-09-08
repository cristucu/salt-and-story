from django.urls import path

from . import views


app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("latest/", views.recipe_latest, name="latest"),
    path("add/", views.recipe_create, name="add"),
    path("<int:pk>/edit/", views.recipe_update, name="edit"),
    path("<int:pk>/", views.recipe_detail, name="detail"),
]

