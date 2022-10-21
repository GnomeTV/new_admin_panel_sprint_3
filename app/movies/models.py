from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .models_mixins import TimeStampedMixin, UUIDMixin
from django.utils.translation import gettext_lazy as _


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('title'), max_length=255)
    description = models.TextField(verbose_name=_('description'), null=True,
                                   blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkTypes(models.TextChoices):
        FRESHMAN = 'movie', _('movie')
        SOPHOMORE = 'tv_show', _('tv_show')

    file_path = models.FileField(verbose_name=_('file'), blank=True, null=True,
                                 upload_to='movies/')
    title = models.CharField(verbose_name=_('title'), max_length=255)
    description = models.TextField(verbose_name=_('description'), blank=True,
                                   null=True)
    creation_date = models.DateField(verbose_name=_('creation_date'),
                                     blank=True,
                                     null=True)
    rating = models.FloatField(verbose_name=_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)],
                               null=True)
    type = models.CharField(verbose_name=_('type'), max_length=128,
                            choices=FilmworkTypes.choices)
    genres = models.ManyToManyField(verbose_name=_('genres'), to=Genre,
                                    through='GenreFilmwork')
    persons = models.ManyToManyField(verbose_name=_('persons'), to=Person,
                                     through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(name='film_work_rating_idx', fields=['rating', ])
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(verbose_name=_('film_work'), to=Filmwork,
                                  on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey(verbose_name=_('genres'), to=Genre,
                              on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.genre.name

    class Meta:
        db_table = 'genre_film_work'
        verbose_name = _('Genre Filmwork')
        verbose_name_plural = _('Genres Filmworks')
        constraints = [
            models.UniqueConstraint(name='genre_film_work_idx',
                                    fields=['genre', 'film_work', ]),
        ]


class PersonFilmwork(UUIDMixin):
    class RoleTypes(models.TextChoices):
        actor = 'actor', _('actor')
        writer = 'writer', _('writer')
        director = 'director', _('director')

    film_work = models.ForeignKey(verbose_name=_('film_work'), to=Filmwork,
                                  on_delete=models.CASCADE)
    person = models.ForeignKey(verbose_name=_('persons'), to=Person,
                               on_delete=models.CASCADE)
    role = models.CharField(verbose_name=_('role'), null=True,
                            choices=RoleTypes.choices, max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person.full_name

    class Meta:
        db_table = 'person_film_work'
        verbose_name = _('Person Filmwork')
        verbose_name_plural = _('Persons Filmworks')
        constraints = [
            models.UniqueConstraint(name='film_work_person_idx',
                                    fields=['film_work', 'person', 'role', ]
                                    ),
        ]
