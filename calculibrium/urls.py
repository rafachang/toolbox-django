from django.urls import path

from . import views

app_name = 'calculibrium'
urlpatterns = [
    path("", views.index, name="index"),
    path("change_theme/", views.change_theme, name="change_theme"),
    path("<str:categoria_componente>/list", views.list, name="list"),
    path("<str:categoria_componente>/select", views.select, name="select"),

    path("inverter", views.inverter, name="inverter"),
    path("cable/ac", views.cable_ac, name="cable_ac"),

    path("roof_disponibilization", views.roof_disponibilization, name="roof_disponibilization"),
    path("structure/kwp", views.structure_kwp, name="structure_kwp"),
    path("structure/un", views.structure_un, name="structure_un"),
    
    path("find-cable-ac/<current_max>/<distance>/<int:connection_type>", views.find_cable_ac, name="find_cable_ac"),
    path("find-circuit-breaker/<current>/<int:connection_type>", views.find_circuit_breaker, name="find_circuit_breaker"),
    path("find-modules-amount/<int:module_pk>/<power_plant>", views.find_modules_amount, name="find_modules_amount"),
    path("find-inverters/<power_plant>", views.find_inverters, name="find_inverters"),
]