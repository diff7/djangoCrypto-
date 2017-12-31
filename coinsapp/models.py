# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

#basically, we are forming a database structure for our сsutom data here for our


class Coin(models.Model):
    coin_name = models.CharField(max_length=10)

class Value(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    # ForeignKey, That tells Django each Value is related to a single Coin
    coin_value = models.FloatField(default=0)
    # FloatField is the same as DecimalField but different
    get_time = models.DateTimeField('request time')
