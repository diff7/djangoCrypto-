from __future__ import absolute_import, unicode_literals
import ccxt
from coinsapp.models import Coin, Value, Coinproperties
import requests
from datetime import datetime, timedelta
from coinsapp.models import Coin, Value, Coinproperties
from datetime import datetime, timedelta

def get_coinmarketcap():
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    coinmarketcap_data=r.json()
    return(coinmarketcap_data)

def get_my_symbols():
    exchange = ccxt.binance  ({ 'verbose': True })
    exchange.load_markets()

    binance_symbols=exchange.symbols
    binance_symbols.remove('123/456')
    binance_symbols.remove('CHAT/BTC')
    binance_symbols.remove('CHAT/ETH')
    binance_symbols.remove('BCD/BTC')
    binance_symbols.remove('BCD/ETH')

    binance_symbols_clean=[]
    for ticker in binance_symbols:
         binance_symbols_clean.append(ticker.split('/')[0])

    coinmarketcap_data=get_coinmarketcap()
    coinmarkectcap_symbols=[]
    coinmarkectcap_symbols=[c['symbol'] for c in coinmarketcap_data]

    my_symbols=[]
    my_symbols=[s for s in binance_symbols_clean if s in coinmarkectcap_symbols]

    return(my_symbols)


def get_my_coin_data():
    t=datetime.now()-timedelta(hours=2)

    coinmarketcap_data=get_coinmarketcap()
    my_symbols=get_my_symbols()

    for ticker in coinmarketcap_data:
        if ticker['symbol'] in my_symbols:

            price = ticker['price_usd']
            price_change = ticker['percent_change_1h']
            basevolume = ticker['market_cap_usd']


            if (price is not None) and (price_change is not None) and (basevolume is not None):

                d=datetime.now()
                d=d.replace(tzinfo=None)
                for_values=Coin.objects.get(coin_name=ticker['symbol'])


                v=for_values.value_set.create(coin_value=price, reqtime=datetime.now(),coin_basevolume=basevolume)
                v.save()



def make_coin_properties():
    t=datetime.now()-timedelta(hours=1)
    t_half=datetime.now()-timedelta(minutes=30)
    all_coins=Coin.objects.all()
    for ticker in all_coins:
        volume=ticker.value_set.filter(reqtime__gt=t).order_by('reqtime')
        Last_volume=volume.last().coin_basevolume
        First_volume=volume.first().coin_basevolume

        Last_price=volume.last().coin_value
        First_price=volume.first().coin_value

        price_change=(Last_price-First_price)/First_price*100
        volume_change=(Last_volume-First_volume)/First_volume*100
        #!!!Publisher.objects.filter(id=1).update(name='Apress Publishing')
        p=ticker.coinproperties_set.update(coin_perchange=price_change,volume_change=volume_change)

        volume_hafl=ticker.value_set.filter(reqtime__gt=t_half).order_by('reqtime')

        Last_price_half=volume_hafl.last().coin_value
        First_price_half=volume_hafl.first().coin_value

        Last_volume_half=volume.last().coin_basevolume
        First_volume_half=volume.first().coin_basevolume

        price_change_half=(Last_price_half-First_price_half)/First_price_half*100
        volume_change_half=(Last_volume_half-First_volume_half)/First_volume_half*100

        p_half=ticker.coinproperties_set.update(coin_change_half=price_change_half,volume_change_half=volume_change_half)


def update_my_markers():
    my_symbols=get_my_symbols()
    coins=Coin.objects.all().values('coin_name')
    coins_to_delete = [c['coin_name'] for c in coins if c['coin_name'] not in my_symbols]
    print(my_symbols)
    print(coins_to_delete)

    for ticker in coins_to_delete:
        coin=Coin.objects.get(coin_name=ticker)
        coin.delete()
        print(ticker)

    for ticker in  my_symbols:
        c=Coin.objects.update_or_create(coin_name=ticker)

def delete_old_values():
    t=datetime.now()-timedelta(hours=5)
    c=Value.objects.filter(reqtime__lt=t)
    c.delete()
