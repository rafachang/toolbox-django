# Generated by Django 4.1.3 on 2023-11-24 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0028_rename_dbcable_dbcableflex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbinverter',
            name='connection_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculibrium.dbconnection'),
        ),
    ]