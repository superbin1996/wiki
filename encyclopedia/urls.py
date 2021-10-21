from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.newpage, name="newpage"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("wiki/edit/<str:name>", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("randompage/", views.randompage, name="randompage")
]


