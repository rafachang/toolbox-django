from django.urls import path

from . import views

app_name = 'calculibrium'
urlpatterns = [
    path("", views.index, name="index"),
    path("change_theme/", views.change_theme, name="change_theme"),
    path("<str:categoria_componente>/list", views.list, name="list"),
    path("<str:categoria_componente>/select", views.select, name="select"),

    path("inverter", views.inverter, name="inverter"),
    
    path("roof_disponibilization", views.roof_disponibilization, name="roof_disponibilization"),
    path("structure/kwp", views.structure_kwp, name="structure_kwp"),
    path("structure/un", views.structure_un, name="structure_un"),
]