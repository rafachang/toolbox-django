import math
from calculibrium.model.component import Inverter, Module
from calculibrium.model.table import Table
from calculibrium.model.structure import Structure

class PowerPlant:
    def __init__(self, customer: str, module: Module, power: float, inverter_table: bool = False, inverter: Inverter = None):
        self.customer = customer
        self.module = module
        self.inverter = inverter
        self.inverter_table = inverter_table
        self.power = power
        self.modules_amount = None
        self.real_power = None
        self.calc_modules_amount()
        self.table = Table(self.module, self.modules_amount)
        self.structures = None

    def calc_modules_amount(self):
        self.modules_amount = round(self.power/(self.module.potencia/1e3)/3)*3
        self.real_power = self.modules_amount*self.module.potencia/1e3

    def calc_structure(self):
        arr = []
        self.array_tables = []
        for qtd_modulo, qtd_table in zip(self.table.tables['qtd_modulo'], self.table.tables['qtd_mesas']):
            if not arr:
                obj = Structure(self.module, qtd_modulo, qtd_table, self.inverter_table)
            else:
                obj = Structure(self.module, qtd_modulo, qtd_table, False)
            self.array_tables.append([qtd_modulo, qtd_table])
            arr.append(obj)
        
        self.structure_total = Structure(self.module, 0, 0, False)
        # print(self.structure_total.bom)
        for idx, i in enumerate(arr):
            cont = 0
            for key, value in i.bom.items():
                self.structure_total.bom[key]['quantidade'] += value['quantidade']
                cont += 1
        self.structure_total.calc_bases()
        arr.append(self.structure_total)
        self.bases = arr[-1].bases
        self.structures = arr
        

    def calc_concrete(self, height_buried, ray_buried, height_exposed, ray_exposed):
        self.volume_buried = math.pi*(ray_buried**2)*height_buried
        self.volume_exposed = math.pi*(ray_exposed**2)*height_exposed
        self.volume_per_base = self.volume_buried+self.volume_exposed
        self.volume_total = math.ceil(self.volume_per_base*self.bases*1.1)
        

if __name__ == '__main__':
    power_plant = PowerPlant('Rafael Chang', Module(0,0,0,0,0,0,0,0,540,2261,1134,35,0,0,0,0), 105.00)
    power_plant.calc_structure()
    print(power_plant.table.tables)