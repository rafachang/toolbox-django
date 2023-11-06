from audioop import reverse
from django.db import models

# Create your models here.

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
