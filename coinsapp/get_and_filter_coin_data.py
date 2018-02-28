from __future__ import absolute_import, unicode_literals
import ccxt
from coinsapp.models import Coin, Value, Coinproperties
import requests
from datetime import datetime, timedelta
from coinsapp.models import Coin, Value, Coinproperties, Gems
from coinsapp.my_telegram import send_to_telegram

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

    binance_symbols.remove('RCN/ETH')
    binance_symbols.remove('RCN/BTC')
    binance_symbols.remove('BAT/ETH')
    binance_symbols.remove('BAT/BTC')
    binance_symbols.remove('BAT/BNB')
    binance_symbols.remove('RCN/BNB')

    binance_symbols_clean=[]
    for ticker in binance_symbols:
         binance_symbols_clean.append(ticker.split('/')[0])

    coinmarketcap_data=get_coinmarketcap()
    coinmarkectcap_symbols=[]
    coinmarkectcap_symbols=[c['symbol'] for c in coinmarketcap_data]

    my_symbols=[]
    my_symbols=[s for s in binance_symbols_clean if s in coinmarkectcap_symbols]

    return(my_symbols)

def get_coin_ful_name():
    full_name=[]
    name=0
    my_symbols=get_my_symbols()
    coinmarketcap_data=get_coinmarketcap()
    for ticker in coinmarketcap_data:
        if ticker['symbol'] in my_symbols:
            name=(str(ticker['symbol'])+" "+str(ticker['name']))

            full_name.append(name)

    return(full_name)



def update_my_markers():
    all_names=get_coin_ful_name()
    my_symbols=get_my_symbols()
    for name in all_names:
        c=Coin.objects.update_or_create(coin_ticker=name)
        print(name)
        if Coin.objects.filter(coin_ticker=str(name)).count() > 1:

            row.delete()

    coins=Coin.objects.all().values('coin_ticker')
    coins_to_delete = [c['coin_ticker'] for c in coins if c['coin_ticker'] not in all_names]

    print(coins_to_delete)
    for ticker in coins_to_delete:
        coin=Coin.objects.filter(coin_ticker=ticker)
        coin.delete()



def get_my_coin_data():
    t=datetime.now()-timedelta(hours=2)
    all_names=get_coin_ful_name()
    coinmarketcap_data=get_coinmarketcap()
    my_symbols=get_my_symbols()

    for ticker in coinmarketcap_data:
        if ticker['symbol'] in my_symbols:

            price = ticker['price_usd']

            if price is not None:

                d=datetime.now()
                d=d.replace(tzinfo=None)
                coins=Coin.objects.get(coin_ticker=str(ticker['symbol'])+" "+str(ticker['name']))

                window=10
                sMa=0
                if coins.value_set.order_by('-reqtime').count()>window:
                    for  smas in coins.value_set.order_by('-reqtime')[:window]:
                        sMa=sMa+smas.coin_value
                sMa=sMa/window


                v=coins.value_set.create(coin_value=price, reqtime=datetime.now(), sma=sMa)


                v.save()


def make_coin_properties():
    t=datetime.now()-timedelta(hours=2)
    t_half=datetime.now()-timedelta(minutes=10)
    coins=Coin.objects.exclude(value__coin_value__isnull=True)

    for symbol in coins:

        volume=symbol.value_set.filter(reqtime__gt=t).order_by('reqtime')

        #PRICE CHANGE 2 HOURS
        Lastprice=volume.last().coin_value
        Firstprice=volume.first().coin_value
        price_change=(Lastprice-Firstprice)/Firstprice*100

        volume_half=symbol.value_set.filter(reqtime__gt=t_half).order_by('reqtime')

        #PRICE CHANEG 10 MIN
        if volume_half.count() > 2:
            Last_pricehalf=volume_half.last().coin_value
            First_pricehalf=volume_half.first().coin_value
            price_changehalf=(Last_pricehalf-First_pricehalf)/First_pricehalf*100
            p=symbol.coinproperties_set.update_or_create(coin=symbol.coin_ticker,  defaults={'coin_change':price_change, 'coin_changehalf':price_changehalf })

        price=symbol.value_set.last().coin_value
        sma=symbol.value_set.last().sma
        time=symbol.value_set.last().reqtime
        if price  <  sma-0.01*price and symbol.coinproperties_set.last().coin_changehalf>0:
            dip=(sma-price)/sma*100
            print(dip)
            Gems.objects.update_or_create(gem_name=symbol.coin_ticker, defaults={'gemStartPrice':price,'gemDip':dip,'gemReqtime':time, 'coinid':symbol.id})
            message='Potential ' + str(round(dip, 2)) + '%  DIP, check the graph here: <a href="http://139.59.127.165/'+str(symbol.id)+'">'+str(symbol.coin_ticker)+'</a>'
            print(message)
            send_to_telegram(message)
        elif Gems.objects.filter(gem_name=symbol.coin_ticker).exists():
             Gems.objects.get(gem_name=symbol.coin_ticker).delete()





def delete_old_values():
    t=datetime.now()-timedelta(hours=12)
    c=Value.objects.filter(reqtime__lt=t)
    c.delete()
