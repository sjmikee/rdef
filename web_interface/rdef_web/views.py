from django.shortcuts import render
from rdef_web.forms import UserProfileInfoForm, LoginForm, UserForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rdef_web.tables import UrlsTable, WLTable, BLTable
from rdef_web.models import urls, whitelist, blacklist
from django.contrib.auth import authenticate
from django.db.models import Count
from chartit import DataPool, Chart
import signal

# Create your views here.
p = None
TERM = signal.SIGTERM
#ratelimit = RateLimitMixin()


def index(request):
    msg = ''
    import asyncio
    import subprocess
    global p
    global TERM

    async def tcp_echo_client(message):
        try:
            reader, writer = await asyncio.open_connection(
                '127.0.0.1', 8888)

            print(f'Send: {message!r}')
            writer.write(message.encode())

            data = await reader.read(100)
            returned_value = data.decode()
            reversed_value = ''.join(chr(ord(a) ^ ord(b))
                                     for a, b in zip(returned_value, 'admin_channel_rdef'))
            print(reversed_value)
            if reversed_value != message:
                msg = 'WRONG ANSWER'
            else:
                msg = ('UP')

            print('Close the connection')
            writer.close()
            return msg
        except Exception as e:
            msg = 'DOWN'
            return msg

    @login_required
    def start_proxy_server(request):
        import os
        global p

        path = os.getcwd()
        parent = os.path.join(path, os.pardir)
        fullpath = (os.path.join(os.path.abspath(parent), "main.py"))
        p = subprocess.Popen('python {}'.format(fullpath),
                             cwd=os.path.abspath(parent), shell=False)

    @login_required
    def stop_proxy_server(request):
        import os
        global p
        pid = p.pid
        os.kill(pid, TERM)
        print(f"########### KILLED {pid} ##########")

    if request.method == 'POST' and 'turn_on' in request.POST:
        start_proxy_server(request)
    elif request.method == 'POST' and 'turn_off' in request.POST:
        stop_proxy_server(request)

    msg = asyncio.run(tcp_echo_client('D4f{gb]@67gd#(Gdl;'))
    return render(request, 'rdef_web/index.html', {'msg': msg})


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    msg = None
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')
        if password == confirm_password:
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                registered = True
                return HttpResponseRedirect(reverse('index'))
            else:
                msg = 'Not valid'
                return render(request, 'rdef_web/registration.html',
                              {'user_form': user_form,
                               'registered': registered,
                               'msg': msg})
        else:
            msg = 'passwords don\'t match'
            return render(request, 'rdef_web/registration.html',
                          {'user_form': user_form,
                           'registered': registered,
                           'msg': msg})
    else:
        user_form = UserForm()
    return render(request, 'rdef_web/registration.html',
                  {'user_form': user_form,
                           'registered': registered,
                           'msg': msg})


def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                msg = 'Your account is not active'
        else:
            msg = 'Invalid credentials'
            return render(request, 'rdef_web/login.html', {'form': form, 'msg': msg})
    else:
        return render(request, 'rdef_web/login.html', {'form': form, 'msg': msg})


@login_required
def urls_table(request):
    table = UrlsTable(urls.objects.all())

    return render(request, "rdef_web/urls_table.html", {
        "table": table
    })


@login_required
def item_remove(request):
    return render(request, "rdef_web/urls_tables.html")


@login_required
def whitelist_table(request):
    table = WLTable(whitelist.objects.all())

    return render(request, "rdef_web/urls_table.html", {
        "table": table
    })


@login_required
def blacklist_table(request):
    table = BLTable(blacklist.objects.all())

    return render(request, "rdef_web/urls_table.html", {
        "table": table
    })


@login_required
def charts(request):
    # Blacklist charts datasources
    blacklist_data_by_protocol = DataPool(
        series=[{'options': {'source': blacklist.objects.extra({'protocol': "protocol"}).values('protocol').annotate(url=Count('url'))}, 'terms': ['protocol', 'url']}])

    blacklist_data_by_date = DataPool(
        series=[{'options': {'source': blacklist.objects.extra({'date': "date(date)"}).values('date').annotate(url=Count('url'))}, 'terms': ['date', 'url']}])

    blacklist_data_by_time = DataPool(
        series=[{'options': {'source': blacklist.objects.extra({'time': "time(time)"}).values('time').annotate(url=Count('url'))}, 'terms': ['time', 'url']}])

    # Whitelist charts datasources
    whitelist_data_by_protocol = DataPool(
        series=[{'options': {'source': whitelist.objects.extra({'protocol': "protocol"}).values('protocol').annotate(url=Count('url'))}, 'terms': ['protocol', 'url']}])

    whitelist_data_by_date = DataPool(
        series=[{'options': {'source': whitelist.objects.extra({'date': "date(date)"}).values('date').annotate(url=Count('url'))}, 'terms': ['date', 'url']}])

    whitelist_data_by_time = DataPool(
        series=[{'options': {'source': whitelist.objects.extra({'time': "time(time)"}).values('time').annotate(url=Count('url'))}, 'terms': ['time', 'url']}])

    # Blacklist charts
    bl_cht_pt = Chart(
        datasource=blacklist_data_by_protocol,
        series_options=[{'options': {'type': 'column',
                                     'stacking': 'True'}, 'terms': {'protocol': ['url', ]}}],
        chart_options={'title': {'text': 'Blacklist by protocol'}, 'xAxis': {'title': {'text': 'protocol'}}})

    bl_cht_date = Chart(
        datasource=blacklist_data_by_date,
        series_options=[{'options': {'type': 'line',
                                     'stacking': 'False'}, 'terms': {'date': ['url', ]}}],
        chart_options={'title': {'text': 'Blacklist by date'}, 'xAxis': {'title': {'text': 'date'}}})

    bl_cht_time = Chart(
        datasource=blacklist_data_by_time,
        series_options=[{'options': {'type': 'line',
                                     'stacking': 'False'}, 'terms': {'time': ['url', ]}}],
        chart_options={'title': {'text': 'Blacklist by time'}, 'xAxis': {'title': {'text': 'time'}}})

    # Whitelist charts
    wl_cht_pt = Chart(
        datasource=whitelist_data_by_protocol,
        series_options=[{'options': {'type': 'column',
                                     'stacking': 'True'}, 'terms': {'protocol': ['url', ]}}],
        chart_options={'title': {'text': 'Whitelist by protocol'}, 'xAxis': {'title': {'text': 'protocol'}}})

    wl_cht_date = Chart(
        datasource=whitelist_data_by_date,
        series_options=[{'options': {'type': 'line',
                                     'stacking': 'True'}, 'terms': {'date': ['url', ]}}],
        chart_options={'title': {'text': 'Whitelist by date'}, 'xAxis': {'title': {'text': 'date'}}})

    wl_cht_time = Chart(
        datasource=whitelist_data_by_time,
        series_options=[{'options': {'type': 'line',
                                     'stacking': 'True'}, 'terms': {'time': ['url', ]}}],
        chart_options={'title': {'text': 'Whitelist by time'}, 'xAxis': {'title': {'text': 'time'}}})

    return render(request, "rdef_web/charts.html", {"charts": [bl_cht_pt, bl_cht_date, bl_cht_time, wl_cht_pt, wl_cht_date, wl_cht_time]})
