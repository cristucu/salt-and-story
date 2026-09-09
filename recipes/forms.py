

from typing import ClassVar

from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe

        fields = (
            "title",
            "description",
            "ingredients",
            "instructions",
            "cooking_time",
        )

        widgets: ClassVar[dict] = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Give your recipe a title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Tell us a little about this recipe",
                }
            ),
            "ingredients": forms.Textarea(
                attrs={
                    "placeholder": "List the ingredients, one per line",
                }
            ),
            "instructions": forms.Textarea(
                attrs={
                    "placeholder": "Describe the steps, one per line",
                }
            ),
            "cooking_time": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 30 minutes",
                }
            ),
        }

