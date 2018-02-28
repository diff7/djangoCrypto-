# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# to add Coin model to admin panel

from .models import Coin, Value, Coinproperties, Gems

admin.site.register(Coin)
admin.site.register(Value)
admin.site.register(Coinproperties)
admin.site.register(Gems)
