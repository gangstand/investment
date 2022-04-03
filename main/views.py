from django.shortcuts import render
from django.http import HttpResponse
from .forms import Invest
from .main import kurse, strat1, strat2, strat4, strat3
import random
import investpy

def index(request):
    if request.method == "POST":
        action = request.POST.get("ticer")
        country = request.POST.get("country")
        Countries = request.POST.get("Countries")
        data_start = request.POST.get("data_start")
        data_end = request.POST.get("data_end")
        action_buy = request.POST.get("action_buy")
        print(country)
        print(Countries)
        exc = 'Неверная форма ввода!'
        if Countries == 'strategy1':
            list_info = kurse(action, country).split("-")
            df = investpy.get_stock_historical_data(stock=action,
                                                    country=country,
                                                    from_date=data_start,
                                                    to_date=data_end)
            close = list(df['Close'].values)

            effect = (float(close[-1])-float(action_buy))/100
            try:
                return render(request, 'main/final.html', {'div':list_info[0], 'price':close[-1], 'strat':strat1(action, country, data_start, data_end), 'effect':round(effect, 2)})
            except:
                return render(request, 'main/final.html', {'strat': exc})

        if Countries == 'strategy2':
            try:
                list_info = kurse(action, country).split("-")
                df = investpy.get_stock_historical_data(stock=action,
                                                        country=country,
                                                        from_date=data_start,
                                                        to_date=data_end)
                close = list(df['Close'].values)

                effect = (float(close[-1]) - float(action_buy)) / 100
                return render(request, 'main/final.html', {'div':list_info[0], 'price':close[-1], 'strat':strat2(action, country, data_start, data_end), 'effect':round(effect, 2)})
            except:
                return render(request, 'main/final.html', {'strat': exc})
        if Countries == 'strategy3':
            try:
                list_info = kurse(action, country).split("-")
                df = investpy.get_stock_historical_data(stock=action,
                                                        country=country,
                                                        from_date=data_start,
                                                        to_date=data_end)
                close = list(df['Close'].values)

                effect = (float(close[-1]) - float(action_buy)) / 100
                return render(request, 'main/final.html', {'div':list_info[0], 'price':close[-1], 'strat':strat3(action, country, action_buy), 'effect':round(effect, 2)})
            except:
                return render(request, 'main/final.html', {'strat': exc})
        if Countries == 'strategy4':
            window1=3
            window2=10
            list_info = kurse(action, country).split("-")
            try:
                effect = strat4(action, country, data_start, data_end, window1, window2)
                df = investpy.get_stock_historical_data(stock=action,
                                                        country=country,
                                                        from_date=data_start,
                                                        to_date=data_end)
                close = list(df['Close'].values)

                effects = (float(close[-1]) - float(action_buy)) / 100
                return render(request, 'main/final.html', {'div': list_info[0], 'price': close[-1],
                                                  'strat': effect, 'effect':round(effects, 2)})
            except:
                return render(request, 'main/final.html', {'strat': exc})
    else:
        invest = Invest()
        return render(request, "main/index.html", {"form": invest})

