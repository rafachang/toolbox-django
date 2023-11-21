
import csv
from calculibrium.models import *

def importar_dados(caminho_do_csv):
    with open(caminho_do_csv, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Ignorar cabeçalho se houver um
        next(leitor_csv, None)
        
        for linha in leitor_csv:
            # DBModule.objects.create(
            #     module_id=linha[0],
            #     model=linha[1],
            #     nominal_power=linha[3],
            #     operating_voltage=linha[4],
            #     operating_current=linha[5],
            #     open_circuit_voltage=linha[6],
            #     short_circuit_current=linha[7],
            #     max_system_voltage=linha[8],
            #     length=linha[9],
            #     width=linha[10],
            #     height=linha[11],
            #     weight=linha[12],
            #     price=linha[13],
            #     brand=linha[14],
            #     component=linha[15],
            #     bifacial=linha[16],
            # )
            DBInverter.objects.create(
                model = linha[0],
                cc_max_pv_power = linha[1],
                cc_max_input_voltage = linha[2],
                cc_startup_input_voltage = linha[3],
                cc_mppt_voltage_range_min = linha[4],
                cc_mppt_voltage_range_max = linha[5],
                cc_max_input_current = linha[6],
                cc_max_short_circuit_current = linha[7],
                cc_num_mppt = linha[8],
                cc_isc_max_main = linha[9],
                ca_isc_max_secundary = linha[10],
                cc_num_inputs = linha[11],
                cc_num_inputs_main = linha[12],
                cc_num_inputs_secundary = linha[13],
                cc_mppt_desbalanced = linha[14],
                ca_power = linha[15],
                ca_connection_type = linha[16],
                ca_current = linha[17],
                ca_max_current = linha[18],
                length = linha[19],
                width = linha[20],
                height = linha[21],
                weight = linha[22],
                price = linha[23],
                brand_id = linha[24],
                ca_voltage_id = linha[25],
                component_id = linha[26]
            )

importar_dados('data.csv')

