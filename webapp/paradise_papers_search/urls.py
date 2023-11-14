"""paradise_papers_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path

from django.conf import settings

# Loading plotly Dash apps script
import paradise_papers_search.settings.dash_app

urlpatterns = [
    re_path('', include('django.contrib.auth.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    re_path(r'^fetch/', include('fetch_api.urls')),
    re_path(r"^admin/", admin.site.urls),
    re_path('dashboard/', include('dashboard.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
