# Generated by Django 4.1.3 on 2023-11-24 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0023_alter_dbbrand_options_alter_dbcable_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBConnection',
            fields=[
                ('connection_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Conexão',
                'verbose_name_plural': 'Conexões',
            },
        ),
        migrations.RemoveField(
            model_name='dbinverter',
            name='ca_connection_type',
        ),
        migrations.CreateModel(
            name='DBCircuitBreaker',
            fields=[
                ('circuit_breaker_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('poles', models.IntegerField()),
                ('current', models.FloatField()),
                ('length', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('height', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('connection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculibrium.dbconnection')),
            ],
            options={
                'verbose_name': 'Circuit Breaker',
                'verbose_name_plural': 'Circuit Breakers',
            },
        ),
    ]
