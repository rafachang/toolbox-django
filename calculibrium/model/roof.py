import math
import pandas as pd
from calculibrium.models import DBComponent


class Roof:
    def __init__(self, module: DBComponent, modules_amount: int):
        self.module = module
        self.modules_amount = modules_amount
        self.calculate_kit_dimension()
        self.calculate()
        self.layout()

    def calculate_kit_dimension(self):
        self.kit_length = 4*(self.module.largura+7)-7
        self.kit_width = self.module.comprimento
    #    print(self.kit_length)
    #    print(self.kit_width)

    def calculate_rows_amount(self, alpha):
        z = self.modules_amount/4
        x = self.kit_width
        y = self.kit_length
        return math.sqrt((z*(x+7)-1007)/(alpha*(y+1e3)))

    def calculate(self):
        self.rows_amount = int(round(self.calculate_rows_amount(3),0))
        self.rows_amount = 1 if self.rows_amount <= 0 else self.rows_amount
        self.cols_amount = self.modules_amount/4/self.rows_amount
        self.roof_length = math.ceil(self.cols_amount)*(self.kit_width+7)-7+2e3
        self.roof_width = self.rows_amount*(self.kit_length+1e3)+1e3
    
    def layout(self):
        self.row = [math.floor(self.cols_amount)]*self.rows_amount
        for i in range(int(round(self.cols_amount % 1*self.rows_amount, 0))):
            self.row[i] = math.ceil(self.cols_amount)
       
# if __name__ == '__main__':
#     arr = []
#     for i in range(1,700):
#         roof = Roof(DBComponent.objects.get(cdcrm=1750512), i*4)
#         dict = {}
#         dict['modules_amount'] = i*4
#         dict['power'] = i*0.54*4
#         dict['rows_amount'] = roof.rows_amount
#         dict['cols_amount'] = roof.cols_amount
#         dict['roof_length'] = roof.roof_length
#         dict['roof_width'] = roof.roof_width
#         dict['display_kits'] = roof.row
#         dict['conferencia'] = sum(roof.row)-i
#         arr.append(dict)
#     df = pd.DataFrame(arr)
#     print(df)
#     df.to_csv('roof.csv', index=False)
