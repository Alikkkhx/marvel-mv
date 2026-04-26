from django.contrib import admin
from .models import Phase, Movie, WatchedStatus

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ru', 'year', 'phase', 'release_date', 'director')
    list_filter = ('phase', 'year')
    search_fields = ('title', 'title_ru', 'description_en', 'description_ru', 'director')
    ordering = ('release_date', 'title')

@admin.register(WatchedStatus)
class WatchedStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'is_watched')
    list_filter = ('is_watched', 'user')
