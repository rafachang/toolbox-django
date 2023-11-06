import math
from calculibrium.model.component import Module

class Structure():
    def __init__(self, module: Module, module_amount: int, table_amount, inverter_table) -> None:
        self.module = module
        self.module_amount = module_amount
        self.table_amount = table_amount
        self.inverter_table = inverter_table
        self.bom = {
                '5603112':{'descricao': 'PERFIL UE P1 - PILAR 150X60X2,65X1500MMM', 'quantidade': 0},
                '5603113':{'descricao': 'PERFIL UE P2 - PILAR 150X60X2,65X723MM', 'quantidade': 0},
                '5601003':{'descricao': 'FUNDACAO VERGALHO 2M CA-50 8,00MM CORTE DOBRA', 'quantidade': 0},
                '5601002':{'descricao': 'FUNDACAO ESTRIVO DIAM.340MM CA-60 5,00MM NERVURADO', 'quantidade': 0},
                '5601001':{'descricao': 'FUNDACAO ESTRIVO DIAM.190MM CA-60 4,20MM NERVURADO', 'quantidade': 0},
                '5601101':{'descricao': 'ARAME RECOZIDO 18 TORCIDO', 'quantidade': 0},
                '5603111':{'descricao': 'PERFIL L1" X 1/8"x 875 - MAO FRANCESA', 'quantidade': 0},
                '5603115':{'descricao': 'PERFIL UE 100X50X17X2,25X 6000 - VIIGA', 'quantidade': 0},
                '5603001':{'descricao': 'CT1 E CT2  - L1" X 1/8"X3250MM - CT1 - CONTRAVENTAMENTO', 'quantidade': 0},
                '5603002':{'descricao': 'CT3 E CT4 - L1" X  1/8"X 3090MM - CONTRAVENTAMENTO', 'quantidade': 0},
                '5603110':{'descricao': 'PERFIL L 2"X 1/8"X100MM - APOIO DE TERCAS', 'quantidade': 0},
                '5603011':{'descricao': 'TUBO 80X40X1.5 X 6,010MM  - TERCAS CENTRAIS GALVANIZADAS À FOGO', 'quantidade': 0},
                '1810101':{'descricao': 'BARRA ROSCADA 3/8"', 'quantidade': 0},
                '1000207':{'descricao': 'PARAFUSO SEXTAVADO 1/2" X 1.1/4" SEXT 3/4" G.A13UNC R.I. ZINFOGO', 'quantidade': 0},
                '1030002':{'descricao': 'ARRUELA LISA 1/2\' ZINFOGO', 'quantidade': 0},
                '1020004':{'descricao': 'PORCA ASTM A563 G.A 13UNC 1/2" SEXT 3/4" ZINFOGO', 'quantidade': 0},
                '1000209':{'descricao': 'PARAFUSO 3/8"X1.1/2" SEXT 9/16" RP A307 G.A 16UNC ZINFOGO', 'quantidade': 0},
                '1030006':{'descricao': 'ARRUELA LISA 7/16 - para o parafuso 3/8', 'quantidade': 0},
                '1020007':{'descricao': 'PORCA SEXTAVADA 3/8" SEXT 9/16" ASTM A563 G.A 16UNC ZINFOGO', 'quantidade': 0},
                '1000212':{'descricao': 'PARAFUSO INOX SEXTAVADO RI M8X20 DIN933 A2', 'quantidade': 0},
                '1020009':{'descricao': 'PORCA INOX 304 SEXT M8 FLANGEADA C/ SERRILHA DIN6923 A2', 'quantidade': 0},
                '1000304':{'descricao': 'PARAFUSO BROC PB 12 14X1" HWH 5/16" TCP3 ECOSEAL', 'quantidade': 0},
                '1000102':{'descricao': 'PARAFUSO FIXADOR HARDBOLT M10X150MM SEXT 9/16\' ECOSEAL 10K', 'quantidade': 0},
                '5601303':{'descricao': 'BROCA TRYCUT SDS 10X255X315MM', 'quantidade': 0},
                '5603009':{'descricao': 'CANTONEIRA 10CM MODELO 1 (OBILONGO DIST. 55MM)', 'quantidade': 0},
                '5605015':{'descricao': 'TAMPA PONTEIRA PVC 80X40', 'quantidade': 0},
                '7010006':{'descricao': 'FITA INSUTAPE (ARREDONDAR DE 30 EM 30 M)', 'quantidade': 0},
                '5603010':{'descricao': 'SPRAY DE GALVANIZACAO A FRIO', 'quantidade': 0},
                '5601201':{'descricao': 'TUBO PAPELAO 4000 X 400 X 5', 'quantidade': 0}
            }
        self.tam_tot = 0
        self.calculate()

    def calculate(self):
        self.tam_tot = ((self.module.largura*self.module_amount)-21+(7*self.module_amount))/3; 'Largura total da mesa em [mm]'
        aux = math.floor(self.tam_tot/3005); 'quantidade de quantos espaçamentos de 3005 há no tamanho total'
        gap = self.tam_tot-(aux*3005); 'Sobra em [mm] do espaçamento'
        qtd_eixo = aux+1
        qtd_barra = None

        if gap>2400:
            self.gap_final = 500
            qtd_eixo += 1
            self.tam_sp = self.tam_tot-6010
            qtd_barra = (round((self.tam_sp/3005))+2)*3*self.table_amount
        else:
            self.gap_final = gap/2
            self.tam_sp = (self.tam_tot-(2*(3005+self.gap_final)))
            qtd_barra = ((self.tam_sp/3005)+4)*3*self.table_amount

        if(self.inverter_table):
            self.bom['1810101']['quantidade'] = 1
            qtd_barra += 3
        else:
            self.bom['1810101']['quantidade'] = 0

        self.qtd_ctv = round(qtd_eixo/3)

        self.bom['5603112']['quantidade'] = round(qtd_eixo*self.table_amount, 2)
        self.bom['5603113']['quantidade'] = round(self.bom['5603112']['quantidade'], 2)
        self.bom['5601003']['quantidade'] = round((self.bom['5603112']['quantidade']+self.bom['5603113']['quantidade'])*4, 2)
        self.bom['5601002']['quantidade'] = round((self.bom['5603112']['quantidade']+self.bom['5603113']['quantidade'])*5, 2)
        self.bom['5601001']['quantidade'] = round((self.bom['5603112']['quantidade']+self.bom['5603113']['quantidade'])*6, 2)
        self.bom['5601101']['quantidade'] = round((self.bom['5603112']['quantidade']+self.bom['5603113']['quantidade'])/2.5, 2)
        self.bom['5603111']['quantidade'] = round(self.bom['5603112']['quantidade']*4, 2)
        self.bom['5603115']['quantidade'] = round(self.bom['5603112']['quantidade'], 2)
        self.bom['5603001']['quantidade'] = round(self.qtd_ctv*self.table_amount*2, 2)
        self.bom['5603002']['quantidade'] = round(self.bom['5603001']['quantidade'], 2)
        self.bom['5603110']['quantidade'] = round(self.bom['5603115']['quantidade']*6, 2)
        self.bom['5603011']['quantidade'] = round(qtd_barra, 2)
        self.bom['1000207']['quantidade'] = round(math.ceil((self.bom['5603112']['quantidade']+self.bom['5603113']['quantidade'])/5)*5, 2)
        self.bom['1030002']['quantidade'] = round(self.bom['1000207']['quantidade']*2, 2)
        self.bom['1020004']['quantidade'] = round(self.bom['1000207']['quantidade'], 2)
        self.bom['1000209']['quantidade'] = round(math.ceil((((self.bom['5603111']['quantidade']*2)+self.bom['5603110']['quantidade']+(self.bom['5603001']['quantidade']*8))*1.03)/5)*5, 2)
        self.bom['1030006']['quantidade'] = round(self.bom['1000209']['quantidade']*2 if self.inverter_table else (self.bom['1000209']['quantidade']*2)+12*self.bom['1810101']['quantidade'], 2)
        self.bom['1020007']['quantidade'] = round(self.bom['1000209']['quantidade'], 2)
        self.bom['1000102']['quantidade'] = round(self.bom['5603112']['quantidade']*8, 2)
        self.bom['5601303']['quantidade'] = round(math.ceil((self.bom['1000102']['quantidade']/60)), 2)
        self.bom['5603009']['quantidade'] = round((self.module_amount/3+1)*6*self.table_amount, 2)
        self.bom['1000304']['quantidade'] = round(math.ceil((((self.bom['5603110']['quantidade']*2)+(self.bom['5603009']['quantidade']*2))*1.05)/5)*5, 2)
        self.bom['1000212']['quantidade'] = round(math.ceil((self.bom['5603009']['quantidade']*2)/5)*5, 2)
        self.bom['1020009']['quantidade'] = round(self.bom['1000212']['quantidade'], 2)
        self.bom['5605015']['quantidade'] = round(self.table_amount*12, 2)
        self.bom['7010006']['quantidade'] = round(math.ceil((self.bom['5603009']['quantidade']*0.1)/30)*30, 2)
        self.bom['5603010']['quantidade'] = round(math.ceil(qtd_barra/80), 2)
        self.bom['5601201']['quantidade'] = round(self.bom['5603112']['quantidade']*0.8, 2)
        self.calc_bases

    def calc_bases(self):
        self.bases = self.bom['5603112']['quantidade']*2

#if __name__ == "__main__":
#    obj = Structure(1048,300,1,False)
#    print(obj.get_bill())