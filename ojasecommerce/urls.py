from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /backend/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('categories/', include('categories.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('profile/', include('profile.urls')),
    path('aboutus/', include('about_us_farm.urls')),
    path('backend/', include('backend.urls')),
    path('gallery/', include('gallery.urls')),
    path('robots.txt', robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
