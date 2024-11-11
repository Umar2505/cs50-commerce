from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("<int:list_id>", views.lists, name="list"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed", views.closed, name="closed"),
    path("categories/<str:cat>", views.cats, name="cats")
]
