from django.shortcuts import get_object_or_404, render

from .models import Recipe


def home(request):
    return render(request, "home.html")


def recipe_list(request):
    recipes = Recipe.objects.all().order_by("title")

    return render(
        request,
        "recipes/recipe_list.html",
        {"recipes": recipes},
    )


def recipe_latest(request):
    recipes = Recipe.objects.all().order_by("-created_at")

    return render(
        request,
        "recipes/recipe_latest.html",
        {"recipes": recipes},
    )

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    return render(
        request,
        "recipes/recipe_detail.html",
        {"recipe": recipe},
    )
