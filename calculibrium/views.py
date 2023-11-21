import json
from django.http import Http404, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import FieldError
from django.shortcuts import render
import pandas as pd
from calculibrium.model.power_plant import PowerPlant
from calculibrium.model.roof import Roof
from calculibrium.model.inverter import get_cheaper
from calculibrium.model.table import Table
from .models import DBComponent, DBBrand, DecimalEncoder

def index(request: WSGIRequest):
    
    return render(request, "calculibrium/index.html")

def change_theme(request: WSGIRequest):
    theme = request.session.get('theme', 'light')
    if theme == 'light':
        request.session['theme'] = 'dark'
    else:
        request.session['theme'] = 'light'
    return JsonResponse({'success': True})

def list(request: WSGIRequest, categoria_componente):
    try:
        list = DBComponent.objects.filter(categoria_componente__exact=categoria_componente)
    except DBComponent.DoesNotExist:
        raise Http404('Component does not exist!')
    return render(request, "calculibrium/list.html", {"list": list})

def select(request: WSGIRequest, categoria_componente):
    componentes = DBComponent.objects.filter(categoria_componente=categoria_componente)
    marcas = DBBrand.objects.filter(dbcomponent__in=componentes).distinct()
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    if request.method == 'POST':
        print(request.POST.getlist('container-inverters'))
    return render(request, 'calculibrium/cable_ac.html', {'marcas_json': marcas_json, 'componentes_json': componentes_json})

def inverter(request: WSGIRequest):
    componentes = DBComponent.objects.filter(categoria_componente='IN')
    marcas = DBBrand.objects.filter(dbcomponent__in=componentes).distinct()
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    return render(request, 'calculibrium/inverter.html',
                  {
                      'marcas_json': marcas_json,
                      'componentes_json': componentes_json,
                  })

def find_inverter(request: WSGIRequest):
    inv = get_cheaper(203.68)
    json_data = json.dumps(inv, cls=DjangoJSONEncoder)
    return JsonResponse({'data': json_data})

def roof_disponibilization(request: WSGIRequest):
    roof = Roof(DBComponent.objects.get(cdcrm=1750512), 93)
    return render(request, "calculibrium/index.html")

def structure_kwp(request: WSGIRequest):
    componentes = DBComponent.objects.filter(categoria_componente='PN', largura__gt=0)
    marcas = DBBrand.objects.filter(dbcomponent__in=componentes).distinct()
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    power_plant = PowerPlant('Rafael Chang', DBComponent.objects.get(cdcrm=1750512), 103.68)
    if request.method == 'POST':
        items = {}
        for chave, valor in request.POST.items():
            items[chave] = valor
        module = DBComponent.objects.get(pk=items['slcModuleModel'])
        power_plant = PowerPlant(items['txt_customers_name'], 
                                 module,
                                 float(items['txt_power_plant_power']))
        # power_plant.inverter_table = True if items['chk_inverter'] else False
        power_plant.inverter_table = True if request.POST.get('chk_inverter') else False
        power_plant.calc_structure()
        power_plant.calc_concrete(1.6, 0.15, 0.4, 0.2)
    return render(request, "calculibrium/structure_kwp.html", 
                  {
                    "power_plant": power_plant,
                    'brands': marcas_json,
                    'components': componentes_json,
                   })

def structure_un(request: WSGIRequest):
    componentes = DBComponent.objects.filter(categoria_componente='PN', largura__gt=0)
    marcas = DBBrand.objects.filter(dbcomponent__in=componentes).distinct()
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    power_plant = PowerPlant('Rafael Chang', DBComponent.objects.get(cdcrm=1750512), 0)
    if request.method == 'POST':
        items = {}
        for chave, valor in request.POST.items():
            items[chave] = valor
        try:
            modules_amount = [int(i) for i in request.POST.getlist('txt_modules_amount')]
            tables_amount = [int(i) for i in request.POST.getlist('txt_tables_amount')]
        except:
            raise FieldError('Calculo não realizado, verifique os campos e tente novamente!')
        module = DBComponent.objects.get(pk=items['slcModuleModel'])
        power_plant = PowerPlant(items['txt_customers_name'], 
                                 module,
                                 0)
        power_plant.modules_amount = sum([int(i)*int(tables_amount[idx]) for idx, i in enumerate(modules_amount)])
        power_plant.real_power = power_plant.modules_amount*float(power_plant.module.potencia)/1e3
        power_plant.table.tables['qtd_modulo'] = modules_amount
        power_plant.table.tables['qtd_mesas'] = tables_amount
        power_plant.table.tables['dimensions'] = None
        power_plant.inverter_table = True if request.POST.get('chk_inverter') else False
        power_plant.calc_structure()
        power_plant.calc_concrete(1.6, 0.15, 0.4, 0.2)
        return render(request, "calculibrium/structure_un.html", {
            "power_plant": power_plant,
            'brands': marcas_json,
            'components': componentes_json,
            "tables": zip(modules_amount, tables_amount)
        })
    
    return render(request, "calculibrium/structure_un.html", 
                  {
                      "power_plant": power_plant,
                      'brands': marcas_json,
                      'components': componentes_json
                      })

