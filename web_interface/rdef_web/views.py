from django.shortcuts import render
from rdef_web.forms import UserProfileInfoForm, LoginForm, UserForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rdef_web.tables import UrlsTable
from rdef_web.models import urls
from django.contrib.auth import authenticate
import signal

# Create your views here.
p = None
TERM = signal.SIGTERM
#ratelimit = RateLimitMixin()

'''def index(request):
    msg = ''
    if request.method == 'POST' and 'start_server' in request.POST:
        #from subprocess import call
        #call(["python", "C:\\Users\\sjmike\\Desktop\\RealTimeProject\\rdef\\main.py"])
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("localhost", 9998))
            msg = 'UP'
            s.close()
        except socket.error as err:
            msg = err
            s.close()
        return render(request, 'rdef_web/index.html', {'msg': msg})
    return render(request, 'rdef_web/index.html', {'msg': msg})'''


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
    # return render(request, 'rdef_web/index.html', {'msg': msg})


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


'''
def user_login(request):
    form = LoginForm(request.POST or None)
    user = None
    msg = None
    #global ratelimit

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            #ratelimit = RateLimitMixin()
            # user = ratelimit.limited_authenticate(
            #    request=request, username=username, password=password)
            #user = authenticate(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            print('authenticated')
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = 'Your account is not active'
            else:
                msg = 'Invalid credentials'
                return render(request, 'rdef_web/login.html', {'form': form, 'msg': msg})
        except:
            msg = 'Wrong login limit reached'
            return render(request, 'rdef_web/login.html', {'form': form, 'msg': msg})
    else:
        return render(request, 'rdef_web/login.html', {'form': form, 'msg': msg})
'''


@login_required
def urls_table(request):
    table = UrlsTable(urls.objects.all())

    return render(request, "rdef_web/urls_table.html", {
        "table": table
    })
