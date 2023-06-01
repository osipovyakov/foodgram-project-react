import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import TokenCreateSerializer, UserSerializer
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingList, Tag)
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class ImageField64 (serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomTokenCreateSerializer(TokenCreateSerializer):
    settings.LOGIN_FIELD = User.USERNAME_FIELD


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context['request'].user.id, follower=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta():
        model = RecipeIngredient
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_recipeingredient.all')
    image = ImageField64()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'author',
                  'name',
                  'text',
                  'image',
                  'cooking_time',
                  'ingredients',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart',)

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context['request'].user.id, recipe=obj.id).exists()


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id',
                  'amount',)


class RecipeCreateUpdateSerializer(RecipeSerializer):
    tags = serializers.ListField()
    ingredients = RecipeIngredientCreateSerializer(many=True)

    def create(self, validate_data):
        ingredients = validate_data.pop('ingredients')
        tags = validate_data.pop('tags')
        recipe = Recipe.objects.create(
            **validate_data,
            author=self.context['request'].user
        )
        for ingredient in ingredients:
            id, amount = ingredient.values()
            new_ingredient = Ingredient.objects.get(id=id)
            RecipeIngredient.objects.create(ingredient=new_ingredient,
                                            recipe=recipe, amount=amount)

        for tag in tags:
            new_tag = Tag.objects.get(id=tag)
            RecipeTag.objects.create(recipe=recipe, tag=new_tag)
        return recipe

    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.text = validate_data.get('text', instance.text)
        instance.cooking_time = validate_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validate_data.get('image', instance.image)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        RecipeTag.objects.filter(recipe=instance).delete()
        ingredients = validate_data.get('ingredients')
        tags = validate_data.get('tags')
        for ingredient in ingredients:
            id, amount = ingredient.values()
            new_ingredient = get_object_or_404(Ingredient, id=id)
            RecipeIngredient.objects.create(
                ingredient=new_ingredient,
                recipe=instance, amount=amount
            )
        for tag in tags:
            new_tag = get_object_or_404(Tag, id=tag)
            RecipeTag.objects.create(
                recipe=instance, tag=new_tag
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class SubscribeUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
        extra_kwargs = {'follower': {'read_only': True},
                        'user': {'read_only': True}}

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context['request'].user.id, follower=obj.follower.id
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.follower.id)
        serializer = SubscribeRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.follower.id).count()
