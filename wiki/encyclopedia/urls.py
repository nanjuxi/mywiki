from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("NewEntry", views.NewEntry, name="NewEntry"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("get/<str:pagetitle>", views.get, name="get"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("rand", views.rand, name="rand")
    ]