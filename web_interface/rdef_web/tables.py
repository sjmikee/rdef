import django_tables2 as tables
from rdef_web.models import urls, whitelist, blacklist


class UrlsTable(tables.Table):
    class Meta:
        model = urls
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url', 'user', 'time', 'protocol')


class WLTable(tables.Table):
    class Meta:
        model = whitelist
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url')


class BLTable(tables.Table):
    class Meta:
        model = blacklist
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url')
