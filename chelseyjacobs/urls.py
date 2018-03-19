from django.conf.urls import url

from . import views


# this loads the landing page at chelseyjacobs.com (index.html)
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
