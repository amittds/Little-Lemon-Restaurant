# Generated by Django 5.0.7 on 2024-11-01 10:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_order_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='token_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]