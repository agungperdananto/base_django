from django.conf.urls import url

from .views import signup_view


app_name='account'

urlpatterns = [
    url(r'^signup/?$', signup_view, name='signup')
]
