# Generated by Django 4.1.3 on 2023-11-16 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0005_dbvoltage_dbmodule_dbinverter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbmodule',
            name='module_efficiency',
        ),
        migrations.RemoveField(
            model_name='dbmodule',
            name='operating_temperature',
        ),
    ]
