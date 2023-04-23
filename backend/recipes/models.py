from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient (models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=50, verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=50
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Recipe (models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название рецепта')
    text = models.TextField(blank=False, verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        blank=False
    )
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        blank=False,
        null=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        blank=False,
        verbose_name='Слаг рецепта'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=False,
        verbose_name='Таг рецепта'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт в избранном'
    )

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'

    def __str__(self):
        return f'{self.recipe} в Избранном у {self.user}'


class ShopingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoping_list',
        verbose_name='Рецепт для похода в магазин'
    )

    class Meta:
        verbose_name = 'Рецепт для похода в магазин'
        verbose_name_plural = 'Рецепты для похода в магазин'

    def __str__(self):
        return f'{self.recipe} для магазина у {self.user}'
