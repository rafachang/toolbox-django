from audioop import reverse
from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class DBBrand(models.Model):

    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Marca")
        verbose_name_plural = ("Marcas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})

class DBComponent(models.Model):
    component_id = models.AutoField(primary_key=True)
    supplypoint = models.CharField(max_length=3,null=True)
    categoria_componente = models.CharField(max_length=3,null=True)
    cdgrupo = models.CharField(max_length=4,null=True)
    grupo = models.CharField(max_length=255,null=True)
    cdsubgrupo = models.CharField(max_length=6,null=True)
    subgrupo = models.CharField(max_length=255,null=True)
    descricao = models.CharField(max_length=255)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE, null=True)
    modelo = models.CharField(max_length=255,null=True)
    unidmedida = models.CharField(max_length=2,null=True)
    procedencia = models.CharField(max_length=255,null=True)
    cdantigo = models.CharField(max_length=255,null=True)
    cdcrm = models.CharField(max_length=50)
    preferencial = models.BooleanField(null=True)
    conexao = models.CharField(max_length=1,null=True)
    potencia = models.DecimalField(max_digits=100, decimal_places=3,null=True)
    comprimento = models.IntegerField(null=True)
    largura = models.IntegerField(null=True)
    altura = models.IntegerField(null=True)
    correnteac = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    correntedc = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    tensaoac = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    tensaodc = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    orientacao_mptt = models.IntegerField(null=True)
    preco = models.DecimalField(max_digits=100, decimal_places=4,null=True)
    qtd_estoque = models.DecimalField(max_digits=100, decimal_places=4,null=True)
    inv_requer_stringbox = models.BooleanField(null=True)
    cabo_ac_mm = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    stringbox_qtd_inout = models.IntegerField(null=True)
    qtd_disjuntores = models.IntegerField(null=True)
    tensao_primario = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    tensao_secundario = models.DecimalField(max_digits=100, decimal_places=2,null=True)
    status = models.CharField(max_length=255,null=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

    def __str__(self):
        return self.descricao
    
    def get_absolute_url(self):
        return reverse("componente_detail", kwargs={"pk": self.pk})

    def to_dict(self):
        return model_to_dict(self)

# region Database Exclusivo site

class DBMaterial(models.Model):

    material_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    resistivity = models.FloatField(default=0)

    class Meta:
        verbose_name = ("Material")
        verbose_name_plural = ("Materiais")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("DBMaterial_detail", kwargs={"pk": self.pk})

class DBConnection(models.Model):

    connection_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Conexão")
        verbose_name_plural = ("Conexões")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("DBConnection_detail", kwargs={"pk": self.pk})

class DBVoltage(models.Model):

    voltage_id = models.AutoField(primary_key=True)
    phase_to_phase = models.IntegerField()
    phase_to_neutral = models.IntegerField()

    class Meta:
        verbose_name = ("Tensão")
        verbose_name_plural = ("Tensões")

    def __str__(self):
        return str(self.phase_to_phase)+'/'+str(self.phase_to_neutral)+' V'

    def get_absolute_url(self):
        return reverse("DBVoltage_detail", kwargs={"pk": self.pk})

class DBCircuitBreaker(models.Model):

    circuit_breaker_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE, default=0)
    connection_type = models.ForeignKey(DBConnection, on_delete=models.CASCADE)
    poles = models.IntegerField()
    current = models.FloatField()

    length = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = ("Circuit Breaker")
        verbose_name_plural = ("Circuit Breakers")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("CircuitBreaker_detail", kwargs={"pk": self.pk})

class DBInverter(models.Model):
    inverter_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE, default=20)
    model = models.CharField(max_length=100)

    cc_max_pv_power = models.DecimalField(max_digits=10, decimal_places=2)
    cc_max_input_voltage = models.DecimalField(max_digits=10, decimal_places=2)
    cc_startup_input_voltage = models.IntegerField(default=0)
    cc_mppt_voltage_range_min = models.IntegerField(default=0)
    cc_mppt_voltage_range_max = models.IntegerField(default=0)
    cc_max_input_current = models.DecimalField(max_digits=10, decimal_places=2)
    cc_max_short_circuit_current = models.DecimalField(max_digits=10, decimal_places=2)
    cc_num_mppt = models.IntegerField(default=0)
    cc_mppt_desbalanced = models.BooleanField(default=0)
    cc_isc_max_main = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ca_isc_max_secundary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cc_num_inputs = models.IntegerField(default=0)
    cc_num_inputs_main = models.IntegerField(null=True)
    cc_num_inputs_secundary = models.IntegerField(null=True)
    
    ca_power = models.DecimalField(max_digits=10, decimal_places=2)
    ca_voltage = models.ForeignKey(DBVoltage, on_delete=models.PROTECT, default=0)
    connection_type = models.ForeignKey(DBConnection, on_delete=models.CASCADE)
    ca_current = models.DecimalField(max_digits=10, decimal_places=2)
    ca_max_current = models.DecimalField(max_digits=10, decimal_places=2)

    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        verbose_name = ("Inversor")
        verbose_name_plural = ("Inversores")

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse("DBInverter", kwargs={"pk": self.pk})

class DBCableFlex(models.Model):
    cable_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    gauge = models.FloatField()
    current = models.FloatField()
    external_diameter = models.FloatField()
    material = models.ForeignKey(DBMaterial, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = ("Cabo Flex")
        verbose_name_plural = ("Cabos Flex")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("DBCable", kwargs={"pk": self.pk})

class DBModule(models.Model):
    module_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    bifacial = models.BooleanField(default=False)
    nominal_power = models.IntegerField()
    operating_voltage = models.FloatField()
    operating_current = models.FloatField()
    open_circuit_voltage = models.FloatField()
    short_circuit_current = models.FloatField()
    max_system_voltage = models.FloatField()
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    price = models.FloatField()
    
    class Meta:
        verbose_name = ("Módulo")
        verbose_name_plural = ("Módulos")

    def __str__(self):
        return (str(self.nominal_power) + ', ' + self.model)

    def get_absolute_url(self):
        return reverse("DBModule_detail", kwargs={"pk": self.pk})

# endregion

# region TODO

class DBCustomer(models.Model):

    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name =  ("Customer")
        verbose_name_plural =   ("Customers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})
class DBPowerPlant(models.Model):

    power_plant_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(DBCustomer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("PowerPlant")
        verbose_name_plural = ("PowerPlants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PowerPlant_detail", kwargs={"pk": self.pk})

class DBOrder(models.Model):

    order_id = models.AutoField(primary_key=True)
    component = models.ForeignKey(DBComponent, on_delete=models.CASCADE)
    power_plant = models.ForeignKey(DBPowerPlant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

# endregion