from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^parse', views.parse),
    url(r'^status', views.status),
]

