# Generated by Django 4.1.3 on 2023-11-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0015_remove_dbinverter_ca_max_power'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbinverter',
            name='cc_max_input_current',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dbinverter',
            name='cc_max_input_voltage',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dbinverter',
            name='cc_max_pv_power',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='dbinverter',
            name='cc_max_short_circuit_current',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
