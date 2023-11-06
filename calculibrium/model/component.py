class Module:
    def __init__(self, component_id, categoria_componente, descricao, brand, modelo, procedencia, cdcrm, preferencial, potencia, comprimento, largura, altura, correntedc, tensaodc, preco, qtd_estoque):
        self.component_id = component_id
        self.categoria_componente = categoria_componente
        self.descricao = descricao
        self.brand = brand
        self.modelo = modelo
        self.procedencia = procedencia
        self.cdcrm = cdcrm
        self.preferencial = preferencial
        self.potencia = potencia
        self.comprimento = comprimento
        self.largura = largura
        self.altura = altura
        self.correntedc = correntedc
        self.tensaodc = tensaodc
        self.preco = preco
        self.qtd_estoque = qtd_estoque

class Inverter:
    def __init__(self, component_id, categoria_componente, descricao, brand, modelo, cdcrm, preferencial, conexao, potencia, comprimento, largura, altura, correnteac, correntedc, tensaoac, tensaodc, orientacao_mptt, preco, qtd_estoque, inv_requer_stringbox, stringbox_qtd_inout):
        self.component_id = component_id
        self.categoria_componente = categoria_componente
        self.descricao = descricao
        self.brand = brand
        self.modelo = modelo
        self.cdcrm = cdcrm
        self.preferencial = preferencial
        self.conexao = conexao
        self.potencia = potencia
        self.comprimento = comprimento
        self.largura = largura
        self.altura = altura
        self.correnteac = correnteac
        self.correntedc = correntedc
        self.tensaoac = tensaoac
        self.tensaodc = tensaodc
        self.orientacao_mptt = orientacao_mptt
        self.preco = preco
        self.qtd_estoque = qtd_estoque
        self.inv_requer_stringbox = inv_requer_stringbox
        self.stringbox_qtd_inout = stringbox_qtd_inout
