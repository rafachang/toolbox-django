import json
import math
import requests
from django.db.models import F, Max
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core import serializers
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404, render
from calculibrium.model.power_plant import PowerPlant
from calculibrium.model.roof import Roof
from calculibrium.model.inverter import get_cheaper
from .models import *

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

def cable_ac(request: WSGIRequest):
    inversores = DBInverter.objects.all()
    marcas = DBBrand.objects.filter(dbinverter__in=inversores).distinct()
    marcas_json = serializers.serialize('json', marcas)
    inversores_json = serializers.serialize('json', inversores)

    if request.method == 'POST':
        inverters = []
        circuit_breakers = []
        cables = []
        inverters_pk = request.POST.getlist('component')
        inverters_amount = [int(x) for x in request.POST.getlist('txt_inverter_amount')]
        distance = float(request.POST.get('txt_distance'))
        current = 0

        for index, (pk, amount) in enumerate(zip(inverters_pk, inverters_amount)):
            inv = get_object_or_404(DBInverter, pk=pk)
            current += inv.ca_current*amount

            response = find_circuit_breaker(request, inv.ca_current, inv.connection_type)
            if response.status_code == 200:
                circuit_breaker = json.loads(response.content.decode('utf-8'))['disjuntor']
            else:
                return response

            distance_request = distance if sum(inverters_amount) == 1 else 15

            response = find_cable_ac(request, circuit_breaker['current'], distance_request, inv.connection_type)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                cable_ac_pt = data['model_pt']
                cable_ac_az = data['model_az']
                cable_ac_vd = data['model_vd']
                distance_pt = data['distance_pt']
                distance_az = data['distance_az']
                distance_vd = data['distance_vd']
            else:
                return response

            inverters.append(['175XXXX', str(inv.model)+' - '+ str(inv.ca_current) + ' A', amount])
            circuit_breakers.append(['150XXXX', str(circuit_breaker['description'])+' - '+str(circuit_breaker['current'])+ ' A', amount])
            cables.append(['217XXXX', cable_ac_pt['description']+' preto - '+ str(cable_ac_pt['current']) + ' A', distance_pt*amount])
            cables.append(['217XXXX', cable_ac_az['description']+' azul - '+ str(cable_ac_az['current']) + ' A', distance_az*amount])
            cables.append(['217XXXX', cable_ac_vd['description']+' verde - '+ str(cable_ac_vd['current']) + ' A', distance_vd*amount])
        else:
            if sum(inverters_amount) > 1:
                response = find_circuit_breaker(request, current, inv.connection_type)
                if response.status_code == 200:
                    circuit_breaker = json.loads(response.content.decode('utf-8'))['disjuntor']
                else:
                    return response

                response = find_cable_ac(request, circuit_breaker['current'], distance, inv.connection_type)
                if response.status_code == 200:
                    data = json.loads(response.content.decode('utf-8'))
                    cable_ac_pt = data['model_pt']
                    distance_pt = data['distance_pt']
                    cable_ac_az = data['model_az']
                    distance_az = data['distance_az']
                    cable_ac_vd = data['model_vd']
                    distance_vd = data['distance_vd']
                else:
                    return response
                circuit_breakers.append(['150XXXX', str(circuit_breaker['description'])+' - '+str(circuit_breaker['current'])+ ' A', 1])
                cables.append(['217XXXX', cable_ac_pt['description']+' preto - '+ str(cable_ac_pt['current']) + ' A', distance_pt])
                cables.append(['217XXXX', cable_ac_az['description']+' azul - '+ str(cable_ac_az['current']) + ' A', distance_az])
                cables.append(['217XXXX', cable_ac_vd['description']+' verde - '+ str(cable_ac_vd['current']) + ' A', distance_vd])
        return render(request, 'calculibrium/cable_ac.html', {
            'inverters': inverters,
            'circuit_breakers': circuit_breakers,
            'cables': cables,
            'marcas_json': marcas_json,
            'inversores_json': inversores_json,
            'distance': distance
            })
    else:
        return render(request, 'calculibrium/cable_ac.html', {'marcas_json': marcas_json, 'inversores_json': inversores_json})

def select(request: WSGIRequest, categoria_componente):
    componentes = DBComponent.objects.filter(categoria_componente=categoria_componente)
    marcas = DBBrand.objects.filter(dbcomponent__in=componentes).distinct()
    marcas_json = serializers.serialize('json', marcas)
    componentes_json = serializers.serialize('json', componentes)
    if request.method == 'POST':
        print(request.POST.getlist('container-inverters'))
    return render(request, 'calculibrium/select_component.html', {'marcas_json': marcas_json, 'componentes_json': componentes_json})

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
                    "grounding": power_plant.table.grounding,
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
        power_plant.table.tables['dimensions'] = power_plant.table.calculate_dimensions(max(modules_amount), sum(tables_amount))
        power_plant.inverter_table = True if request.POST.get('chk_inverter') else False
        power_plant.table.calc_grounding()
        power_plant.calc_structure()
        power_plant.calc_concrete(1.6, 0.15, 0.4, 0.2)
        return render(request, "calculibrium/structure_un.html", {
            "power_plant": power_plant,
            "grounding": power_plant.table.grounding,  
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

# region API's Refatoramento

def find_cable_ac(request, current_max, distance, connection_type):
    try:
        distance_float = float(distance)
    except ValueError:
        return JsonResponse({'message': 'A distância deve ser um número decimal ou inteiro'}, status=400)

    try:
        current_max_float = float(current_max)
    except ValueError:
        return JsonResponse({'message': 'A corrente deve ser um número decimal ou inteiro'}, status=400)

    try:
        max_cable_ac = float(DBCableFlex.objects.aggregate(Max('current'))['current__max'])
    except:
        return JsonResponse({'message': 'Não foi encontrado o maior cabo AC no Banco de Dados'})
    
    current = current_max_float/(current_max_float//max_cable_ac+1)
    cable_per_phase = int(current_max_float//max_cable_ac+1)
    
    try:
        cable_pt = DBCableFlex.objects.filter(material=2, current__gte=current).order_by('current').first()
        if cable_pt is None:
            return JsonResponse({'message': 'Não há cabo AC disponível com a corrente mínima necessária'}, status=404)
        if current >= 109 and cable_per_phase == 1:
            cable_az = DBCableFlex.objects.filter(material=2, gauge__gte=cable_pt.gauge/2).order_by('gauge').first()
            cable_vd = DBCableFlex.objects.filter(material=2, gauge=cable_az.gauge).order_by('gauge').first()
        else:
            cable_az = DBCableFlex.objects.filter(material=2, gauge=cable_pt.gauge).order_by('current').first()
            cable_vd = DBCableFlex.objects.filter(material=2, gauge=cable_az.gauge).order_by('current').first()

    except:
        return JsonResponse({'message': 'Não foi encontrado o Cabo no Banco de Dados'}, status=404)

    phases = 3 if connection_type == 4 else 2
    distance_pt = distance_float*phases*cable_per_phase
    distance_az = distance_float*math.ceil(cable_per_phase/2)
    distance_vd = distance_float*math.ceil(cable_per_phase/2)

    return JsonResponse({
        'model_pt': model_to_dict(cable_pt),
        'distance_pt': distance_pt,
        'model_az': model_to_dict(cable_az),
        'distance_az': distance_az,
        'model_vd': model_to_dict(cable_vd),
        'distance_vd': distance_vd,
        'cable_per_phase': cable_per_phase
        }, status=200)

def find_circuit_breaker(request, current, connection_type):
    try:
      current_float = float(current)
    except:
      return JsonResponse({'message': 'A corrente deve ser um número decimal ou inteiro'}, status=400)
    
    try:
        circuit_breaker = DBCircuitBreaker.objects.filter(connection_type=connection_type
                                                         ).filter(current__gte=current_float
                                                                  ).order_by('current'
                                                                             ).first()
    except:
        return JsonResponse({'message': 'Não foi encontrado o Disjuntor no Banco de Dados'}, status=404)
    
    if circuit_breaker is None:
        return JsonResponse({'message':'Não há Disjuntor que suporte a Corrente Desejada!'}, status=404)

    return JsonResponse({
        'message': 'Sucesso!',
        'disjuntor': model_to_dict(circuit_breaker)
    }, status=200)

def find_modules_amount(request, module_pk, power_plant):

    try:
      power_plant = float(power_plant)
    except:
      return JsonResponse({'message': 'A potência deve ser um número decimal ou inteiro'}, status=400)

    module = get_object_or_404(DBModule, pk=module_pk)

    try:
      module = DBModule.objects.get(pk=module_pk)
    except:
      return JsonResponse({'message': 'Não foi encontrado o Módulo no Banco de Dados'}, status=404)
    
    print(module)
    module_amount = round(power_plant*1e3/float(module.nominal_power)/3, 0)*3

    return JsonResponse({
        'message': 'Sucesso!',
        'module': model_to_dict(module),
        'modules_amount': module_amount
        }, status=200)

def find_inverters(request, power_plant):
    inverters = get_cheaper(float(power_plant))
    if not inverters:
        return JsonResponse({
            'message': 'Inversor não encontrado!'
        })
    return JsonResponse({
        'message':'Sucesso!',
        'inversores': inverters
        }, status=200)

# endregion