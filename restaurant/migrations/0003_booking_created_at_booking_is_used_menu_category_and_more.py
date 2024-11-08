# Generated by Django 5.0.7 on 2024-09-21 07:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_menu_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.CharField(choices=[('Brunch', 'brunch'), ('Appetizer', 'appetizer'), ('Sides', 'sides'), ('Entrees', 'entrees'), ('Specials', 'specials'), ('Vegan', 'vegan'), ('Beverages', 'beverages'), ('Desserts', 'desserts')], default='main_course', max_length=20),
        ),
        migrations.AddField(
            model_name='menu',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unavailable'), (1, 'Available')], default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='comment',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='booking',
            name='guest_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
