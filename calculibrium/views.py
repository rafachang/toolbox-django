from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest
from django.core import serializers
from django.core.exceptions import FieldError
from django.shortcuts import render

from calculibrium.model.power_plant import PowerPlant
from calculibrium.model.component import Module
from .models import DBComponent, DBBrand

def index(request: WSGIRequest):
    return render(request, "calculibrium/index.html")

def list(request: WSGIRequest, categoria_componente):
    try:
        list = DBComponent.objects.filter(categoria_componente__exact=categoria_componente)
    except DBComponent.DoesNotExist:
        raise Http404('Component does not exist!')
    return render(request, "calculibrium/list.html", {"list": list})

def structure_kwp(request: WSGIRequest):
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
        
        
    return render(request, "calculibrium/structure_kwp.html", {"power_plant": power_plant})

def structure_un(request: WSGIRequest):
    power_plant = PowerPlant('Rafael Chang', Module(0,0,0,0,0,0,0,0,540,2261,1134,35,0,0,0,0), 0)
    if request.method == 'POST':
        items = {}
        for chave, valor in request.POST.items():
            items[chave] = valor
        try:
            modules_amount = [int(i) for i in request.POST.getlist('txt_modules_amount')]
            tables_amount = [int(i) for i in request.POST.getlist('txt_tables_amount')]
        except:
            raise FieldError('Calculo não realizado, verifique os campos e tente novamente!')
        power_plant = PowerPlant(items['txt_customers_name'], 
                                 Module(0,0,0,0,0,0,0,0,int(items['txt_module_power']), 2261, int(items['txt_module_width']), 35, 0, 0, 0, 0),
                                 0)
        power_plant.modules_amount = sum([int(i)*int(tables_amount[idx]) for idx, i in enumerate(modules_amount)])
        power_plant.real_power = power_plant.modules_amount*power_plant.module.potencia/1e3
        power_plant.table.tables['qtd_modulo'] = modules_amount
        power_plant.table.tables['qtd_mesas'] = tables_amount
        power_plant.table.tables['dimensions'] = None
        power_plant.inverter_table = True if request.POST.get('chk_inverter') else False
        power_plant.calc_structure()
        power_plant.calc_concrete(1.6, 0.15, 0.4, 0.2)
        return render(request, "calculibrium/structure_un.html", {
            "power_plant": power_plant,
            "tables": zip(modules_amount, tables_amount)
        })

    return render(request, "calculibrium/structure_un.html", {"power_plant": power_plant})

def cable_ac(request: WSGIRequest):
    marcas = DBBrand.objects.all()
    componentes = DBComponent.objects.filter(categoria_componente='IN')
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    return render(request, 'calculibrium/cable_ac.html', {'marcas': marcas, 'componentes': componentes, 'marcas_json': marcas_json, 'componentes_json': componentes_json})

