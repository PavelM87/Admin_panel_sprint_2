from django.contrib import admin
from .models import Filmwork, PersonFilmWork, FilmworkGenre, Person, Genre


class PersonInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person',)
    extra = 0


class GenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating',)
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    ) 
    list_filter = ('type', 'creation_date', 'genres', 'rating',)

    search_fields = ('title', 'description', 'id',)
    
    inlines = [
        PersonInline,
        GenreInline
    ] 


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date',)
    search_fields = ('full_name', 'birth_date',)
    inlines = [
        PersonInline
    ] 


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
