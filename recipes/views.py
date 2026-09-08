from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
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

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            return redirect("recipes:detail", pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/recipe_form.html",
        {"form": form},
    )


@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            form.save()
            return redirect("recipes:detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "recipe": recipe,
        },
    )

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    if request.method == "POST":
        recipe.delete()
        return redirect("recipes:list")

    return render(
        request,
        "recipes/recipe_confirm_delete.html",
        {"recipe": recipe},
    )
