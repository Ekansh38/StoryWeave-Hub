from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    return render(request, 'hub/index.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'hub/login.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        list_of_users = User.objects.all().values_list('username', flat=True)

        if username in list_of_users:
            return render(request, 'hub/signup.html', {
                "message": "Username Already Exists!"
                })

        if password != password_confirm:
            return render(request, 'hub/signup.html', {
                "message": "Passwords Must Match!"
                })

        user = User.objects.create_user(username=username, password=password)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'hub/signup.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
