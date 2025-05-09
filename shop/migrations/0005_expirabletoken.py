# Generated by Django 5.0.1 on 2024-02-05 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('shop', '0004_product_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpirableToken',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authtoken.token')),
                ('expiration_date', models.DateTimeField()),
            ],
            bases=('authtoken.token',),
        ),
    ]
