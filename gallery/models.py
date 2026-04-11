from django.db import models


class GalleryAlbum(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='images')
    title       = models.CharField(max_length=200, blank=True)
    image       = models.ImageField(upload_to='gallery/images/')
    caption     = models.CharField(max_length=300, blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f'Image in {self.album.title}'
