import math
import pandas as pd
if __name__ == '__main__':
    from component import Module
else:
    from calculibrium.model.component import Module


class Table:
    def __init__(self, module: Module, module_amount: int):
        self.module = module
        self.module_amount = module_amount
        self.power_plant_power = self.module_amount*(self.module.potencia/1000)
        self.rows_margin = 5
        self.rows_amount = 0
        self.cable_length = None
        self.electrode = None
        self.splitbolts = None
        self.tables = self.calculate_tables()
        self.calc_grounding()
    
    def calculate_dimensions(self, module_amount, table_amount):
        table_length = (self.module.largura+7)*module_amount/3-7
        table_width = table_amount*((self.module.comprimento+7)*3-7+5e3)-5e3
        angle = math.degrees(math.atan2(table_width,table_length))
        return table_width, table_length, angle

    def calculate_tables(self):
        if self.module_amount <= 300:
            comprimento_max_mesa = (self.module.largura+7)*self.module_amount/3-7
        else:
            comprimento_max_mesa = (self.module.largura+7)*100-7
        largura_mesa = (self.module.comprimento+7)*3-7
        if self.module_amount <= 3000:
            largura_planta_max = round(math.tan(math.radians(50)))*comprimento_max_mesa
        else:
            largura_planta_max = self.calculate_dimensions(300, math.ceil(self.module_amount/300))[0]
        quantidade_mesa_max = math.ceil((largura_planta_max+5e3)/(largura_mesa+5e3))
        quantidade_mesa_min = math.floor(self.module_amount/300)
        if quantidade_mesa_min == 0:
            quantidade_mesa_min=1
        mesas = []
        for i in range(quantidade_mesa_min, quantidade_mesa_max+1, 1):
            # Possui possibilidade de todas as mesas serem iguais
            if self.module_amount/3 % i == 0:
                mesa = {
                    'qtd_modulo': [self.module_amount/i],
                    'qtd_mesas': [i],
                    'dimensions': self.calculate_dimensions(self.module_amount/i, i)
                }
                mesas.append(mesa)
            # Dois estilos de mesa, alteando uma fileira entre elas
            else:
                mesa = {
                    'qtd_modulo': [math.floor(self.module_amount/3/i)*3, math.ceil(self.module_amount/3/i)*3],
                    'qtd_mesas': [i-self.module_amount/3%i, self.module_amount/3%i],
                    'dimensions': self.calculate_dimensions(math.ceil(self.module_amount/3/i)*3, i)
                }
                mesas.append(mesa)
        list_mesa = [mesa for mesa in mesas if ((len(mesa['qtd_mesas']) == 1) and (15 <= mesa['dimensions'][2] <= 45))]
        if not list_mesa:
            list_mesa = [mesa for mesa in mesas if 25 <= mesa['dimensions'][2] <= 45]
        if not list_mesa:
            list_mesa = mesas
        if list_mesa:
            """Se possuir mesas que sua hipotenusa tenha um angulo de entre 25~50º

            Returns:
                _list_: _closest angle to 45_
            """
            closest = None
            for obj in list_mesa:
                if not closest:
                    closest = obj
                if abs(closest['dimensions'][2]-45) > abs(obj['dimensions'][2]-45):
                    closest = obj
            return closest

    def calc_grounding(self):
        # ring_width = self.tables['dimensions'][0]+2e3
        ring_length = self.tables['dimensions'][1]+2e3
        print(self.tables)
        rows_amount = math.ceil(sum(self.tables['qtd_mesas'])/2)
        print('rows_amount:', rows_amount)
        self.cable_length = (rows_amount*ring_length/1e3)+(sum(self.tables['qtd_mesas'])-2 if sum(self.tables['qtd_mesas']) > 2 else 0)*12
        print('cable_length: ', self.cable_length)
        self.electrode = math.ceil(ring_length/12e3)*rows_amount
        print('electrode: ', self.electrode)
        self.elcectodes_connector = self.electrode
        print('elcectodes_connector: ', self.elcectodes_connector)
        self.foundation_connector = self.elcectodes_connector-rows_amount
        print('foundation_connector: ', self.foundation_connector)
        self.splitbolt = self.electrode
        print('splitbolt: ', self.splitbolt)
        # ring_length = self.tables['dimensions'][1]+2e3
        # ring_perimeter = 2*(ring_length+ring_width)
        # middle_connections = math.ceil(sum(self.tables['qtd_mesas'])/3) if sum(self.tables['qtd_mesas']) >= 3 else 0
        # self.cable_length = ring_perimeter+middle_connections*ring_length
        # self.electrode = (middle_connections+2)*math.floor(ring_length/1e4)+(sum(self.tables['qtd_mesas'])-1)*2+4

    def __str__(self) -> str:
        return 'módulos: '+str(self.tables['qtd_modulo'])+'\nmesas: '+str(self.tables['qtd_mesas'])
        
if __name__ == '__main__':
    # table = Table(Module(0,0,0,0,0,0,0,0,540,2261,1134,35,0,0,0,0), 699*3)
    arr = []
    for i in range(700):
        dict = {}
        table = Table(Module(0,0,0,0,0,0,0,0,540,2261,1134,35,0,0,0,0), i*3)
        dict['power_power_plant'] = round(540*3*i/1e3, 2)
        dict['total_modules'] = 3*i
        dict['modules_amount'] = table.tables['qtd_modulo']
        dict['tables_display'] = table.tables['qtd_mesas']
        dict['tables_amount'] = sum(table.tables['qtd_mesas'])
        dict['cable_length'] = table.cable_length
        dict['electrode'] = table.electrode
        dict['elcectodes_connector'] = table.elcectodes_connector
        dict['foundation_connector'] = table.foundation_connector
        dict['splitbolt'] = table.splitbolt
        arr.append(dict)
    df = pd.DataFrame(arr)
    print(df)
    df.to_csv('grounding.csv')