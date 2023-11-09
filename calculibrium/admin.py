from django.contrib import admin
from calculibrium.models import DBComponent, DBBrand, DBCustomer, DBOrder, DBPowerPlant

admin.site.register(DBComponent)
admin.site.register(DBBrand)
admin.site.register(DBCustomer)
admin.site.register(DBOrder)
admin.site.register(DBPowerPlant)