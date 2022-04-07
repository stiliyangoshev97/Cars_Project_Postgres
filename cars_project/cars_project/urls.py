"""cars_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cars_project import views as v

# Importing static and settings for the media url bellow
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name = 'index'),

    path('', include('cars.urls', namespace = 'cars')),
    path('', include('accounts.urls', namespace = 'accounts')),
    path('', include('profiles.urls', namespace = 'profiles')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # This enables to load pictures from the database, like {{ profile.profile_photo.url }}


