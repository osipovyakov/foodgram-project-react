from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

COLORS_PALETTE = [
    ("#F5B151", "breakfast", ),
    ("#BBE2BB", "lunch", ),
    ("#B1A7E2", "dinner", ),
]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    REQUIRED_FIELDS = ['name', 'measurement_unit']

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=50,
        unique=True
    )
    color = ColorField(samples=COLORS_PALETTE)
    slug = models.SlugField(
        verbose_name='Слаг тега',
        max_length=50,
        unique=True
    )

    REQUIRED_FIELDS = ['name', 'color', 'slug']

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe (models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=2000
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        null=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги рецепта'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
        db_index=True
    )

    REQUIRED_FIELDS = ['author', 'name', 'image',
                       'text', 'cooking_time', ]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    amount = models.IntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipeingredient',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_recipeingredient',
        verbose_name='Рецепт'
    )

    REQUIRED_FIELDS = ['amount']

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}-{self.amount}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_recipetag',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipetag',
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipe} : {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Рецепт в избранном'
    )

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipe} в Избранном у {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shoppinglist',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shoppinglist',
        verbose_name='Рецепт для похода в магазин'
    )

    class Meta:
        verbose_name = 'Рецепт для похода в магазин'
        verbose_name_plural = 'Рецепты для похода в магазин'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipe} для магазина у {self.user}'
