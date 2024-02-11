from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Branch, MainStory


def index(request):
    if request.user.is_authenticated:
        return render(request, "hub/index_in.html", {"user": request.user})
    return render(request, "hub/index_out.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember = request.POST.get("remember", None)
        if remember == None:
            remember = False
        elif remember == "on":
            remember = True

        if remember:
            request.session.set_expiry(604800)
        else:
            request.session.set_expiry(0)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    request.session.set_expiry(0)
    return render(request, "hub/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        list_of_users = User.objects.all().values_list("username", flat=True)

        if username in list_of_users:
            return render(
                request, "hub/signup.html", {"message": "Username Already Exists!"}
            )

        if password != password_confirm:
            return render(
                request, "hub/signup.html", {"message": "Passwords Must Match!"}
            )

        user = User.objects.create_user(username=username, password=password)
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "hub/signup.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def main_story(request):
    branches = MainStory.objects.all().order_by("id")
    story_text = ""

    for branch in branches:
        story_text += branch.branch.text_data

    return render(request, "hub/main_story.html", {"story_text": story_text})


@login_required
def create_branch(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        branch = Branch(title=title, text_data=content, author=request.user)
        branch.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "hub/create_branch.html")


@login_required
def view_branches(request):
    branches = Branch.objects.filter(author=request.user)
    return render(request, "hub/view_branches.html", {"branches": branches})


def remember(request):
    print("remembered")
    request.session.set_expiry(604800)
    return HttpResponseRedirect(reverse("index"))


def un_remember(request):
    print("un-remembered")
    request.session.set_expiry(0)
    return HttpResponseRedirect(reverse("index"))
