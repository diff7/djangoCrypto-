from django.shortcuts import render, render_to_response

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
from models import Coin, Value, Coinproperties, Gems
from django.http import Http404
from datetime import datetime, timedelta
import numpy as np
from numpy import convolve

def all_coindata(request):

    coins_list = Coin.objects.order_by('-coinproperties__coin_changehalf')
    properties = Coinproperties.objects.all()
    gems = Gems.objects.all()
    # value_list_recent= value_list_recent["coin_value"]
    context = {'coins_list': coins_list, 'properties':properties, 'gems':gems}
    return render(request, 'coinsapp/index.html', context)

def build_chart(request, coins_id):

    try:
        c = Coin.objects.get(id=coins_id)
        x=[]
        y=[]
        sMa=[]
        nan = float('nan')
        for values in c.value_set.order_by('reqtime'):
            x.append(values.reqtime)
            y.append(values.coin_value)
            if values.sma == 0.0:
                sMa.append(nan)
            else:
                sMa.append(values.sma)
    # create a new plot with a title and axis labels


        def movingaverage (values, window):
            weights = np.repeat(1.0, window)/window
            sma = list(np.convolve(values, weights, 'valid'))

            n=0

            while (n < window-1):
                n=n+1
                nan = float('nan')
                sma.insert(0,nan)
            return sma

        coin_ticker=c.coin_ticker
        p = figure(title=c.coin_ticker, x_axis_label='Time', y_axis_label='Price', x_axis_type='datetime', height=250)

        sma_20 = movingaverage (y, 20)
        p.line( x,sma_20, legend="SMA 20", line_color="green", line_width=1 )

        sma_50 = movingaverage (y, 30)
        p.line( x,sma_50, legend="SMA 50", line_color="pink", line_width=1 )


        p.line( x,sMa, legend="SMA 10", line_color="red", line_width=2  )

        p.toolbar.logo = None
        # add a line renderer with legend and line thickness
        p.line(x, y, legend=c.coin_ticker, line_width=2)
        p.circle(x, y, fill_color="white", size=8)
        p.sizing_mode = 'scale_width'
        p.legend.location = "bottom_left"
        script, div = components(p, CDN)


        x_h=[]
        y_h=[]
        sMa_h=[]
        t=datetime.now()-timedelta(minutes=60)
        for values in c.value_set.filter(reqtime__gt=t).order_by('reqtime'):
            x_h.append(values.reqtime)
            y_h.append(values.coin_value)
            if values.sma == 0.0:
                sMa_h.append(nan)
            else:
                sMa_h.append(values.sma)

        #sma_ = movingaverage (y, 5)
        p_h = figure(title=c.coin_ticker, x_axis_label='Time', y_axis_label='Price', x_axis_type='datetime', height=250)
        p_h.toolbar.logo = None
        # add a line renderer with legend and line thickness
        p_h.line(x_h, y_h, legend=c.coin_ticker, line_color="green", line_width=2)
        p_h.line(x_h, sMa_h, legend="SMA 10",  line_color="red", line_width=1)
        p_h.circle(x_h, y_h, fill_color="white", size=8)
        p_h.sizing_mode = 'scale_width'
        p_h.legend.location = "bottom_left"
        script_h, div_h = components(p_h)
        # output_file("lines.html")
        # show(p)

        c = Coin.objects.get(id=coins_id)
        value = c.value_set.order_by('reqtime')
    except Value.DoesNotExist:
        raise Http404("Coin value does not exist")
    return render(request,'coinsapp/coin_chart.html',
        {'bk_script' : script , 'bk_div' : div, 'h_bk_script':script_h, 'h_bk_div':div_h, 'value':value, 'coin_ticker':coin_ticker} )
