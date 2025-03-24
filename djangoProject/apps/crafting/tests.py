from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from decimal import Decimal

from apps.crates.models import Item
from apps.users.models import UserProfile

from .models import Recipe, RecipeIngredient, CraftingLog


class RecipeModelTests(TestCase):
    def setUp(self):
        # Create a dummy item to be used as the result item for recipes
        self.item = Item.objects.create(name="Test Item")

    def test_str_returns_name(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            result_item=self.item,
            result_quantity=1,
            description="A test recipe"
        )
        self.assertEqual(str(recipe), "Test Recipe")


class RecipeIngredientModelTests(TestCase):
    def setUp(self):
        # Create dummy items and a recipe for testing
        self.ingredient = Item.objects.create(name="Test Ingredient")
        self.result_item = Item.objects.create(name="Result Item")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            result_item=self.result_item,
            result_quantity=1
        )

    def test_str_returns_expected_format(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=3
        )
        expected_str = f"3 x {self.ingredient.name} for {self.recipe.name}"
        self.assertEqual(str(recipe_ingredient), expected_str)

    def test_unique_constraint(self):
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=3
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RecipeIngredient.objects.create(
                    recipe=self.recipe,
                    ingredient=self.ingredient,
                    quantity=5
                )


class CraftingLogModelTests(TestCase):
    def setUp(self):
        # Create a user and a corresponding user profile
        self.user = User.objects.create_user(username="testuser", password="password")
        # Assuming UserProfile has fields: total_items_crafted, rare_items_crafted, and most_crafted_item
        self.profile = UserProfile.objects.create(user=self.user, total_items_crafted=0, rare_items_crafted=0, most_crafted_item="")
        
        # Create an item and a recipe
        self.item = Item.objects.create(name="Test Item")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            result_item=self.item,
            result_quantity=1
        )

    def test_save_updates_profile_for_non_rare(self):
        # Create a crafting log that is not rare
        CraftingLog.objects.create(user=self.user, recipe=self.recipe, rare=False)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.total_items_crafted, 1)
        self.assertEqual(self.profile.rare_items_crafted, 0)
        self.assertEqual(self.profile.most_crafted_item, self.recipe.name)

    def test_save_updates_profile_for_rare(self):
        # Create a crafting log that is marked as rare
        CraftingLog.objects.create(user=self.user, recipe=self.recipe, rare=True)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.total_items_crafted, 1)
        self.assertEqual(self.profile.rare_items_crafted, 1)
        self.assertEqual(self.profile.most_crafted_item, self.recipe.name)

    def test_most_crafted_item_updates_correctly(self):
        # Create another recipe
        recipe2 = Recipe.objects.create(
            name="Another Recipe",
            result_item=self.item,
            result_quantity=1
        )
        # Create two crafting logs for self.recipe and one for recipe2
        CraftingLog.objects.create(user=self.user, recipe=self.recipe, rare=False)
        CraftingLog.objects.create(user=self.user, recipe=self.recipe, rare=False)
        CraftingLog.objects.create(user=self.user, recipe=recipe2, rare=False)
        self.profile.refresh_from_db()
        # The most crafted item should be the one with the highest count
        self.assertEqual(self.profile.most_crafted_item, self.recipe.name)