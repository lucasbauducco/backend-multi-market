# Generated by Django 5.0.1 on 2024-01-29 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='inicio_actividades',
            field=models.DateField(blank=True, null=True),
        ),
    ]
