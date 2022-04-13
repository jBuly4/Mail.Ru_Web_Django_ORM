from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^simple_route/$', views.simple_route),
    url(r'^slug_route/(?P<data>[0-9a-z_-]+)/$', views.slug_route),
    url(r'^sum_route/(?P<num1>-?[\d]+)/(?P<num2>-?[\d]+)', views.sum_route),
    url(r'^sum_get_method/$', views.sum_get_method),
    url(r'^sum_post_method/$', views.sum_post_method),
]
