# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

#basically, we are forming a database structure for our сsutom data here for our


class Coin(models.Model):
    coin_name = models.CharField(max_length=10)

    def __str__(self):
        return self.coin_name

class Value(models.Model):

    coin_basevolume = models.FloatField(default=0)
    coin = models.ForeignKey('Coin', on_delete=models.CASCADE)
    # ForeignKey, That tells Django each Value is related to a single Coin
    coin_value = models.FloatField(default=0)
    # FloatField is the same as DecimalField but different
    reqtime = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return u'value: %s time: %s volume: %s' % (self.coin_value, self.reqtime, self.coin_basevolume)


class Coinproperties(models.Model):
    coin = models.ForeignKey('Coin', on_delete=models.CASCADE)
    coin_perchange = models.FloatField(default=0)
    coin_change = models.FloatField(default=0)
    allvolume = models.FloatField(default=0)
    volumechange = models.FloatField(default=0)
