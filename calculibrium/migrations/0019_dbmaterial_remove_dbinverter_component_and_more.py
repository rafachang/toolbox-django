# Generated by Django 4.1.3 on 2023-11-24 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0018_alter_dbinverter_height_alter_dbinverter_length_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBMaterial',
            fields=[
                ('material_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'DBMaterial',
                'verbose_name_plural': 'DBMaterials',
            },
        ),
        migrations.RemoveField(
            model_name='dbinverter',
            name='component',
        ),
        migrations.RemoveField(
            model_name='dbmodule',
            name='component',
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='max_system_voltage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='open_circuit_voltage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='operating_current',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='operating_voltage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='short_circuit_current',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='dbmodule',
            name='weight',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='DBCable',
            fields=[
                ('cable_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('gauge', models.FloatField()),
                ('current', models.FloatField()),
                ('external_area', models.FloatField()),
                ('resistivity', models.FloatField()),
                ('material', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='calculibrium.dbmaterial')),
            ],
        ),
    ]
