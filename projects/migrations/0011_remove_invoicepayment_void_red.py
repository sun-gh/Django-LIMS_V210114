# Generated by Django 2.2 on 2021-01-12 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20210111_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicepayment',
            name='void_red',
        ),
    ]