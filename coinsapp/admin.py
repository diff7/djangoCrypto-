# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# to add Coin model to admin panel

from .models import Coin

admin.site.register(Coin)
