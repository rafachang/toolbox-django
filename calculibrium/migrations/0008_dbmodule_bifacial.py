# Generated by Django 4.1.3 on 2023-11-16 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculibrium', '0007_alter_dbmodule_component'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbmodule',
            name='bifacial',
            field=models.BooleanField(default=False),
        ),
    ]
