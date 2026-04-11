from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum, GalleryImage


def gallery_list(request):
    albums = GalleryAlbum.objects.filter(is_active=True).prefetch_related('images')
    context = {'albums': albums}
    return render(request, 'gallery/gallery_list.html', context)


def gallery_album(request, slug):
    album = get_object_or_404(GalleryAlbum, slug=slug, is_active=True)
    images = album.images.filter(is_active=True)
    context = {'album': album, 'images': images}
    return render(request, 'gallery/gallery_album.html', context)
