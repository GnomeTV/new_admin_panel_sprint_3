from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, PersonFilmwork, Person


class FilmworkInlineMixin(admin.TabularInline):
    extra = 1


class GenreFilmworkInline(FilmworkInlineMixin):
    model = GenreFilmwork
    extra = 1
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(FilmworkInlineMixin):
    model = PersonFilmwork
    extra = 1
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified',)
    list_filter = ('name', 'created', 'modified',)
    search_fields = ('name', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_filter = ('created', 'modified',)
    search_fields = ('full_name', 'description', 'id',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date',
                    'rating', 'created', 'modified',)
    list_filter = ('type', 'created', 'modified',)
    search_fields = ('title', 'description', 'id',)
