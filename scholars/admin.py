from django.contrib import admin
from .models import Scholar


@admin.register(Scholar)
class ScholarAdmin(admin.ModelAdmin):
    list_display = ('name', 'madhhab', 'status', 'created_at')
    list_filter = ('status', 'madhhab')
    search_fields = ('name', 'biography')
    readonly_fields = ('slug',)
    ordering = ('-created_at',)
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected scholars as Published"
