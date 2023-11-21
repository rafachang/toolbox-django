from django.contrib import admin
from calculibrium.models import DBComponent, DBBrand, DBCustomer, DBInverter, DBOrder, DBPowerPlant, DBModule, DBVoltage

admin.site.register(DBComponent)
admin.site.register(DBBrand)
admin.site.register(DBCustomer)
admin.site.register(DBOrder)
admin.site.register(DBPowerPlant)
admin.site.register(DBInverter)
admin.site.register(DBModule)
admin.site.register(DBVoltage)