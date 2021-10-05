"""LawEnforcement_system URL Configuration

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
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import admin
# import logout view
from management.views import logout_view
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    # note the override comes before the admin URLs below
    path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
    path('admin/', admin.site.urls),
    path('',include('management.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns +=staticfiles_urlpatterns()

admin.site.site_header  =  "Law Enforcement Administration"  
admin.site.site_title  =  "Law Enforcement admin site"
admin.site.index_title  =  "Law Enforcement Admin"
