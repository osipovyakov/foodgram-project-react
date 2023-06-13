from django.contrib import admin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'count',)
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


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_editable = ('color',)
    list_filter = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient', )
    list_editable = ('ingredient', 'amount',)


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag',)
    list_filter = ('tag',)
    list_editable = ('tag',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)


class ShopingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShopingListAdmin)
