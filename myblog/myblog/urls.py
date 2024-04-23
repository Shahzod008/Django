from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from myblog import settings
from car.views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('car.urls')),
]

if settings.DEBUG:    
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns


    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
