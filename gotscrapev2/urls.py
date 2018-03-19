"""gotscrapev2 URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # this is the INITIAL URL LIST
    url(r'^$', include('chelseyjacobs.urls')),
    url(r'^makesandwich/', include('makesandwich.urls')),
    url(r'^gotsv2/', include('gotsv2.urls')),
    url(r'^admin/', admin.site.urls),
]

# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
