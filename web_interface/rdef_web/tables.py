import django_tables2 as tables
from django_tables2.utils import A
from rdef_web.models import urls, whitelist, blacklist


class UrlsTable(tables.Table):

    class Meta:
        model = urls
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url', 'user', 'time', 'protocol')


class WLTable(tables.Table):
    Remove = tables.LinkColumn('rdef_web:WLitem_remove', text='Remove', args=[
        A('pk')], orderable=False, empty_values=())

    class Meta:
        model = whitelist
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url')


class BLTable(tables.Table):
    edit = tables.LinkColumn('rdef_web:BLitem_remove', text='Remove', args=[
                             A('pk')], attrs={'a': {'class': 'btn'}}, orderable=False, empty_values=())

    Move = tables.LinkColumn('rdef_web:BLitem_move_to_WL', text='Move To Whitelist', args=[
                             A('pk')], attrs={'a': {'class': 'btn'}}, orderable=False, empty_values=())

    class Meta:
        model = blacklist
        template_name = "django_tables2/bootstrap.html"
        fileds = ('date', 'url')
