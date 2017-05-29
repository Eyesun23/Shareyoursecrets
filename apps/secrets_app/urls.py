from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^process$', views.process),
    url(r'^like/(?P<id>\d+)/(?P<sentby>\w+)$', views.newLike),
    url(r'^delete/(?P<id>\d+)/(?P<sentby>\w+)$', views.delete),
    url(r'^secrets$', views.secrets),
    url(r'^popular$', views.popular),
    url(r'^logout$', views.logout)
]
