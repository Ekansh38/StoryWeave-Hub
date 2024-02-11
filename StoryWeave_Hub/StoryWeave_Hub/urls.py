from django.contrib import admin
from django.urls import include, path
from hub import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("", views.index, name="index"),
    path("main-story/", views.main_story, name="main_story"),
    path("create-branch/", views.create_branch, name="create_branch"),
    path("view_branches", views.view_branches, name="view_branches"),
    path("remember/", views.remember, name="remember"),
    path("un-remember/", views.un_remember, name="un_remember"),
]
