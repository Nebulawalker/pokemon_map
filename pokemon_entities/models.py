from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название покемона на русском'
    )
    title_en = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Название покемона на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Название покемона на японском'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение покемона'
    )
    description = models.TextField(
        default='Описание в разработке',
        verbose_name='Описание покемона'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
        null=True,
        blank=True,
        verbose_name='Предыдущая эволюция покемона'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.PROTECT,
        verbose_name='Покемон',
        related_name='entities'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата, время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата, время исчезновения'
    )
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень покемона')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье покемона')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила покемона')
    defense = models.IntegerField(null=True, blank=True, verbose_name='Защита покемона')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость покемона')

    def __str__(self):
        return f'{self.pokemon.title_ru} {self.level} lvl.'
