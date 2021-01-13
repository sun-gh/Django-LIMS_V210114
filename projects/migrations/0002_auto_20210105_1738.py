# Generated by Django 2.2 on 2021-01-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyinvoice',
            name='status',
            field=models.CharField(choices=[('applying', '申请中'), ('passed', '已通过'), ('refused', '已拒绝')], default='申请中', max_length=32, verbose_name='状态'),
        ),
    ]