from django.conf.urls import url

from . import views


# these determine urls based on the /gotsv2 root - see gotscrapev2/urls
urlpatterns = [
    url(r'^$', views.gotsv2, name='gotsv2'),
    # url(r'^update/', views.update, name='runupdate'),
    url(r'^graph/', views.graph, name='graph'),
    url(r'^gender-graph/',views.gender_graph_page, name='gender-graph'),
    url(r'^title-graph/',views.title_graph_page, name='title-graph'),
    url(r'^about/',views.about, name='about')
]
