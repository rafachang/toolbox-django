# Generated by Django 4.1.3 on 2023-11-17 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0014_alter_dbinverter_brand_alter_dbinverter_ca_voltage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbinverter',
            name='ca_max_power',
        ),
    ]
