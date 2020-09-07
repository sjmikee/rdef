import django_tables2 as tables
from django_tables2.utils import A
from rdef_web.models import urls, whitelist, blacklist


class UrlsTable(tables.Table):

    class Meta:
        attrs = {
            "class": "mdl-data-table mdl-js-data-table mdl-data-table-default-non-numeric mdl-shadow--2dp"}
        model = urls
        fileds = ('date', 'url', 'user', 'time', 'protocol')


class WLTable(tables.Table):
    Remove = tables.LinkColumn('rdef_web:WLitem_remove', text='Remove', args=[
        A('pk')], attrs={'a': {'class': 'mdl-navigation__link'}}, orderable=False, empty_values=())

    class Meta:
        attrs = {
            "class": "mdl-data-table mdl-js-data-table mdl-data-table-default-non-numeric mdl-shadow--2dp"}
        model = whitelist
        fileds = ('date', 'url', 'remove')


class BLTable(tables.Table):
    edit = tables.LinkColumn('rdef_web:BLitem_remove', text='Remove', args=[
                             A('pk')], attrs={'a': {'class': 'mdl-navigation__link'}}, orderable=False, empty_values=())

    Move = tables.LinkColumn('rdef_web:BLitem_move_to_WL', text='Move To Whitelist', args=[
                             A('pk')], attrs={'a': {'class': 'mdl-navigation__link'}}, orderable=False, empty_values=())

    class Meta:
        attrs = {
            "class": "mdl-data-table mdl-js-data-table mdl-data-table-default-non-numeric mdl-shadow--2dp"}
        model = blacklist
        fileds = ('date', 'url')
