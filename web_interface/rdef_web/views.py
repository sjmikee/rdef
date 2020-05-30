from django.shortcuts import render
from rdef_web.forms import UserProfileInfoForm, LoginForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rdef_web.tables import UrlsTable
from rdef_web.models import urls

# Create your views here.


def index(request):
    return render(request, 'rdef_web/index.html')


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
