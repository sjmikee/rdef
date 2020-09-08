# rdef_web/urls.py
from django.conf.urls import url
from rdef_web.views import user_login, register, user_logout, urls_table, whitelist_table, blacklist_table, charts, BLitem_remove, WLitem_remove, BLitem_move_to_WL, reg_success
from rdef_web import forms
# SET THE NAMESPACE!
app_name = 'rdef_web'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^user_register/$', register, name='user_register'),
    url(r'^reg_success/$', reg_success, name='reg_success'),
    url(r'^user_login/$', user_login, name='user_login'),
    url(r'^user_logout/$', user_logout, name='user_logout'),
    url(r'^urls_table/$', urls_table, name='urls_table'),
    url(r'^whitelist_table/$', whitelist_table, name='whitelist_table'),
    url(r'^blacklist_table/$', blacklist_table, name='blacklist_table'),
    url(r'^charts/$', charts, name='charts'),
    url(r'^BLitem_remove/([0-9]+)/$', BLitem_remove, name='BLitem_remove'),
    url(r'^WLitem_remove/([0-9]+)/$', WLitem_remove, name='WLitem_remove'),
    url(r'^BLitem_move_to_WL/([0-9]+)/$',
        BLitem_move_to_WL, name='BLitem_move_to_WL')
]
