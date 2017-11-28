from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.UniversitiesList.as_view(), name='universities_list'),
]