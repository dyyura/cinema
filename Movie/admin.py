from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height = "100"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category_name')
    inlines = [ReviewInLine, ]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('description', 'image'),)
        }),
        (None, {
            'fields': (('year', 'world', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)

        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url}width="100" height="110"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записи не были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записи не были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change',)

    unpublish.short_descriptions = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url}width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url}width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Cinema'
admin.site.site_header = 'Django Cinema'
