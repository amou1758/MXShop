# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-07 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180907_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscategorybrand',
            name='cagetory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品类目'),
        ),
    ]