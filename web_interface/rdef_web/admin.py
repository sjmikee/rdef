from django.contrib import admin
from rdef_web.models import UserProfileInfo, User, urls, whitelist, blacklist
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(urls)
admin.site.register(whitelist)
admin.site.register(blacklist)
