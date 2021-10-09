from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Human(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=200)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='О нем')
    image = models.ImageField(upload_to='actors/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    tagline = models.CharField(verbose_name='Слоган', max_length=60)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Постер', upload_to='movies/')
    year = models.PositiveIntegerField(verbose_name='Дата выхода', default=2021)
    country = models.CharField(verbose_name='Страна', max_length=40)
    directors = models.ManyToManyField(Human, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Human, verbose_name='Актер', related_name='film_actor')
    genres = models.ManyToManyField(Human, verbose_name='Жанры')
    world = models.DateTimeField(verbose_name='Премьера в мире', default=timezone.now)
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text=' Укажите сумму в Долларах')
    fees_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0,
                                              help_text=' Укажите сумму в Долларах')
    fees_in_world = models.PositiveIntegerField(verbose_name='Сборы в Мире', default=0,
                                                help_text=' Укажите сумму в Долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent_isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Сам фильм', on_delete=models.CASCADE, related_name='movieshots')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадры из Фильма'
        verbose_name_plural = 'Кадры из Фильмов'


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Значение', default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда Рейтинга'
        verbose_name_plural = 'Звёзды Рейтинга'


class Review(models.Model):
    email = models.EmailField(verbose_name='Почта')
    name = models.CharField(verbose_name='Имя', max_length=255)
    text = models.TextField(verbose_name='Отзывы', blank=True)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL,
                               blank=True, null=True, related_name='children')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.name} = {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
