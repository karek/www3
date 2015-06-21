from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^obwod/$', views.obwod_json, name='obwod'),
    url(r'^save/$', views.save, name='save'),
]