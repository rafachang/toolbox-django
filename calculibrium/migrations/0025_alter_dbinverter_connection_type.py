# Generated by Django 4.1.3 on 2023-11-24 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0024_dbconnection_remove_dbinverter_ca_connection_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbinverter',
            name='connection_type',
            field=models.IntegerField(default=0),
        ),
    ]