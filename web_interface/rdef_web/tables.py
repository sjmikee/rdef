import django_tables2 as tables
from rdef_web.models import urls


class UrlsTable(tables.Table):
    class Meta:
        model = urls
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url', 'user', 'time', 'protocol')
