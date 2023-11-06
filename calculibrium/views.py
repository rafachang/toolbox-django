from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from calculibrium.model.power_plant import PowerPlant
from calculibrium.model.component import Module

from .models import DBComponent

def index(request: WSGIRequest):
    return render(request, "calculibrium/index.html")

def list(request: WSGIRequest, categoria_componente):
    try:
        list = DBComponent.objects.filter(categoria_componente__exact=categoria_componente)
    except DBComponent.DoesNotExist:
        raise Http404('Component does not exist!')
    return render(request, "calculibrium/list.html", {"list": list})

def structure(request: WSGIRequest):
    power_plant = PowerPlant('Rafael Chang', Module(0,0,0,0,0,0,0,0,540,2261,1134,35,0,0,0,0), 103.68)
    if request.method == 'POST':
        items = {}
        for chave, valor in request.POST.items():
            items[chave] = valor
        power_plant = PowerPlant(items['txt_customers_name'], 
                                 Module(0,0,0,0,0,0,0,0,int(items['txt_module_power']), 2261, int(items['txt_module_width']), 35, 0, 0, 0, 0),
                                 float(items['txt_power_plant_power']))
        # power_plant.inverter_table = True if items['chk_inverter'] else False
        power_plant.inverter_table = True if request.POST.get('chk_inverter') else False
        power_plant.calc_structure()
        power_plant.calc_concrete(1.6, 0.15, 0.4, 0.2)
        
        
    return render(request, "calculibrium/structure.html", {"power_plant": power_plant})

# txt_customers_name
# txt_module_lenght
# txt_module_power
# txt_power_plant_power
# chk_inverter
# txt_height_buried
# txt_ray_buried
# txt_volume_buried
# txt_height_exposed
# txt_ray_exposed
# txt_volume_exposed
# "calculate"
# "export"