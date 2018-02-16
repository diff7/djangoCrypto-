from __future__ import absolute_import, unicode_literals
from celery import task
from coinsapp.get_and_filter_coin_data import get_my_coin_data, delete_old_values, update_my_markers, make_coin_properties


@task()
def remove_old_values():
    delete_old_values()


@task()
def update_markers():
    update_my_markers()


@task()
def get_coin_data():
    get_my_coin_data()


@task()
def get_coin_properties():
    make_coin_properties()
