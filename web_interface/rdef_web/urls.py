# rdef_web/urls.py
from django.conf.urls import url
from rdef_web.views import user_login, register
from rdef_web import forms
# SET THE NAMESPACE!
app_name = 'rdef_web'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^user_login/$', user_login, name='user_login'),
]
