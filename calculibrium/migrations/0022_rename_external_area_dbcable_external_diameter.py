# Generated by Django 4.1.3 on 2023-11-24 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0021_remove_dbcable_resistivity_dbmaterial_resistivity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dbcable',
            old_name='external_area',
            new_name='external_diameter',
        ),
    ]