# rdef_web/urls.py
from django.conf.urls import url
from rdef_web import views
from rdef_web import forms
# SET THE NAMESPACE!
app_name = 'rdef_web'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, {'template_name': 'login.html', 'authentication_form': forms.LoginForm},
        name='login'),
]
