# Generated by Django 4.1.3 on 2023-11-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0016_alter_dbinverter_cc_max_input_current_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbinverter',
            name='ca_power',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
