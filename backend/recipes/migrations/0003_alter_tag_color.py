# Generated by Django 3.2 on 2023-06-05 19:17

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230604_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#F5B151', 'breakfast'), ('#BBE2BB', 'lunch'), ('#B1A7E2', 'dinner')], default='#F5B151', image_field=None, max_length=18, samples=None),
        ),
    ]
