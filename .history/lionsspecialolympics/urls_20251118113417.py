# realestate_portal/urls.py

from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.sitemaps.views import sitemap 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),   # provides login, logout, password reset views
    path('', include('home.urls')),

    
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)