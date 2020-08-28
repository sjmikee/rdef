# rdef_web/urls.py
from django.conf.urls import url
from rdef_web.views import user_login, register, user_logout, urls_table, whitelist_table, blacklist_table, charts
from rdef_web import forms
# SET THE NAMESPACE!
app_name = 'rdef_web'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^user_register/$', register, name='user_register'),
    url(r'^user_login/$', user_login, name='user_login'),
    url(r'^user_logout/$', user_logout, name='user_logout'),
    url(r'^urls_table/$', urls_table, name='urls_table'),
    url(r'^whitelist_table/$', whitelist_table, name='whitelist_table'),
    url(r'^blacklist_table/$', blacklist_table, name='blacklist_table'),
    url(r'^charts/$', charts, name='charts')
]
