from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update/', views.update, name='runupdate'),
    url(r'^graph/', views.graph, name='graph'),
    url(r'^gender-graph/',views.gender_graph_page, name='gender-graph')
]
