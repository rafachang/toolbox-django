from django.urls import path

from . import views

app_name = 'calculibrium'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:categoria_componente>/list", views.list, name="list"),
    path("structure", views.structure, name="structure"),
]