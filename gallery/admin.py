from django.contrib import admin
from .models import GalleryAlbum, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('image', 'title', 'caption', 'order', 'is_active')


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('album', 'title', 'order', 'is_active')
    list_filter = ('album',)
    list_editable = ('order', 'is_active')
