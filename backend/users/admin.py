from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingList, Tag)
from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'last_name',)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'cooking_time', 'image',)
    list_filter = ('author', 'name', 'tags',)
    inlines = (RecipeIngredientInLine,)
    search_fields = ('name',)

    def count(self, x):
        return Favorite.objects.filter(
            recipe=Recipe.objects.get(id=x.id)).count()


class IngredientAdmin (admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_editable = ('color',)
    list_filter = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class ShopingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShopingListAdmin)
