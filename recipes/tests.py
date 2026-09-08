from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Recipe

User = get_user_model()


class RecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="author",
            password="testpass123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123",
        )

        self.recipe = Recipe.objects.create(
            title="Spaghetti Carbonara",
            description="Classic Italian pasta.",
            ingredients="Pasta, eggs, pecorino, guanciale",
            instructions="Cook pasta and prepare the sauce.",
            cooking_time="30 minutes",
            author=self.user,
        )

    def test_recipe_list_is_public(self):
            response = self.client.get(reverse("recipes:list"))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Spaghetti Carbonara")

    def test_recipe_detail_is_public(self):
        response = self.client.get(
            reverse("recipes:detail", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spaghetti Carbonara")

    def test_anonymous_user_cannot_create_recipe(self):
        response = self.client.get(reverse("recipes:add"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_authenticated_user_can_create_recipe(self):
        self.client.login(
            username="author",
            password="testpass123",
        )

        response = self.client.post(
            reverse("recipes:add"),
            {
                "title": "Apple Pie",
                "description": "Classic apple pie.",
                "ingredients": "Apples, flour, sugar",
                "instructions": "Bake the pie.",
                "cooking_time": "60 minutes",
            },
        )

        self.assertEqual(Recipe.objects.count(), 2)

        recipe = Recipe.objects.get(title="Apple Pie")
        self.assertEqual(recipe.author, self.user)
        self.assertRedirects(
            response,
            reverse("recipes:detail", args=[recipe.pk]),
        )

    def test_author_can_edit_own_recipe(self):
        self.client.login(
            username="author",
            password="testpass123",
        )

        response = self.client.post(
            reverse("recipes:edit", args=[self.recipe.pk]),
            {
                "title": "Updated Carbonara",
                "description": "Updated description.",
                "ingredients": "Updated ingredients",
                "instructions": "Updated instructions",
                "cooking_time": "25 minutes",
            },
        )

        self.recipe.refresh_from_db()

        self.assertEqual(self.recipe.title, "Updated Carbonara")
        self.assertRedirects(
            response,
            reverse("recipes:detail", args=[self.recipe.pk]),
        )

    def test_other_user_cannot_edit_recipe(self):
        self.client.login(
            username="otheruser",
            password="testpass123",
        )

        response = self.client.get(
            reverse("recipes:edit", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_author_can_delete_own_recipe(self):
        self.client.login(
            username="author",
            password="testpass123",
        )

        response = self.client.post(
            reverse("recipes:delete", args=[self.recipe.pk])
        )

        self.assertEqual(Recipe.objects.count(), 0)
        self.assertRedirects(
            response,
            reverse("recipes:list"),
        )

    def test_other_user_cannot_delete_recipe(self):
        self.client.login(
            username="otheruser",
            password="testpass123",
        )

        response = self.client.get(
            reverse("recipes:delete", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Recipe.objects.filter(pk=self.recipe.pk).exists()
        )


    def test_recipe_list_is_sorted_alphabetically(self):
        Recipe.objects.create(
            title="Apple Pie",
            description="Dessert",
            ingredients="Apples",
            instructions="Bake",
            cooking_time="60 minutes",
            author=self.user,
        )

        response = self.client.get(reverse("recipes:list"))

        recipes = list(response.context["recipes"])

        self.assertEqual(recipes[0].title, "Apple Pie")
        self.assertEqual(recipes[1].title, "Spaghetti Carbonara")


    def test_latest_recipes_are_sorted_by_creation_date(self):
        newer_recipe = Recipe.objects.create(
            title="Risotto",
            description="Italian rice dish",
            ingredients="Rice",
            instructions="Cook slowly",
            cooking_time="40 minutes",
            author=self.user,
        )

        response = self.client.get(reverse("recipes:latest"))

        recipes = list(response.context["recipes"])

        self.assertEqual(recipes[0], newer_recipe)
        self.assertEqual(recipes[1], self.recipe)