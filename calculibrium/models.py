from audioop import reverse
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class DBVoltage(models.Model):

    voltage_id = models.AutoField(primary_key=True)
    phase_to_phase = models.IntegerField()
    phase_to_neutral = models.IntegerField()

    class Meta:
        verbose_name = ("DBVoltage")
        verbose_name_plural = ("DBVoltages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DBVoltage_detail", kwargs={"pk": self.pk})

class DBBrand(models.Model):

    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Brand")
        verbose_name_plural = ("Brands")

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
        verbose_name = 'componente'
        verbose_name_plural = 'componentes'

    def __str__(self):
        return self.descricao
    
    def get_absolute_url(self):
        return reverse("componente_detail", kwargs={"pk": self.pk})

    def to_dict(self):
        return model_to_dict(self)

class DBInverter(models.Model):
    inverter_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE)
    component = models.ForeignKey(DBComponent, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)

    cc_max_pv_power = models.IntegerField()
    cc_max_input_voltage = models.IntegerField()
    cc_startup_input_voltage = models.IntegerField()
    cc_num_mppt = models.IntegerField()
    cc_mppt_voltage_range_min = models.IntegerField()
    cc_mppt_voltage_range_max = models.IntegerField()
    cc_max_input_current = models.IntegerField()
    cc_max_short_circuit_current = models.IntegerField()
    cc_num_inputs = ArrayField(models.IntegerField())
    
    ca_power = models.IntegerField()
    ca_max_power = models.IntegerField()
    ca_voltage = models.ForeignKey(DBVoltage, on_delete=models.PROTECT)
    ca_connection_type = models.CharField(max_length=3)
    ca_current = models.DecimalField(max_digits=5, decimal_places=2)
    ca_max_current = models.DecimalField(max_digits=5, decimal_places=2)

    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        verbose_name = ("DBInverter")
        verbose_name_plural = ("DBInverter")

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse("DBInverter", kwargs={"pk": self.pk})

class DBModule(models.Model):
    module_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(DBBrand, on_delete=models.CASCADE)
    component = models.ForeignKey(DBComponent, on_delete=models.CASCADE, null=True)
    model = models.CharField(max_length=100)
    nominal_power = models.IntegerField()
    operating_voltage = models.DecimalField(max_digits=5, decimal_places=2)
    operating_current = models.DecimalField(max_digits=5, decimal_places=2)
    open_circuit_voltage = models.DecimalField(max_digits=5, decimal_places=2)
    short_circuit_current = models.DecimalField(max_digits=5, decimal_places=2)
    max_system_voltage = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        verbose_name = ("DBModule")
        verbose_name_plural = ("DBModules")

    def __str__(self):
        return (self.nominal_power + ', ' + self.model)

    def get_absolute_url(self):
        return reverse("DBModule_detail", kwargs={"pk": self.pk})

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
