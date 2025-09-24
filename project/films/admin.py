from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Genre, Movie, Comment, Profile

# Register your models here.

admin.site.register(Genre)
admin.site.register(Profile)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('text', 'user')
    can_delete = False


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director', 'views', 'year', 'genre', 'get_image')
    list_display_links = ('id', 'name')
    list_editable = ('genre',)
    list_filter = ('genre',)
    search_fields = ('name', 'description', 'genre__name')
    list_per_page = 10
    inlines = [
        CommentInline
    ]
    readonly_fields = ('views',)

    def get_image(self, movie):
        if movie.image:
            return mark_safe(f'<img src="{movie.image.url}" width: "150">')
        else:
            return "-"
        
    get_image.short_description = "Rasmi"

admin.site.register(Movie, MovieAdmin)