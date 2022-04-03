import investpy
import numpy as np
import yfinance as yf
import requests
import matplotlib.pyplot as plt
def kurse(action, country):
    try:
        search_result = investpy.search_quotes(text=action, products=['stocks'],
                                           countries=[country], n_results=1)
        information = search_result.retrieve_information()

        if country == 'Russia':
           stock = action + '.ME'
           ticker_yahoo = yf.Ticker(stock)
        else:
           ticker_yahoo = yf.Ticker(action)
        price = ticker_yahoo.info.get("currentPrice")

        if country == 'Russia':
          return "Дивиденды: "+ str(information["dividend"]) + "-Стоимость: "+ str(price) + "руб"
        else:
          return "Дивиденды: "+ str(information["dividend"])+ "-Стоимость: "+ str(price)+ "$"
    except:
        if country == 'Russia':
           stock = action + '.ME'
           ticker_yahoo = yf.Ticker(stock)
        else:
           ticker_yahoo = yf.Ticker(action)
        price = ticker_yahoo.info.get("currentPrice")

        if country == 'Russia':
          return "Дивиденды: "+ "-Стоимость: "+ str(price) + "руб"
        else:
          return "Дивиденды: "+ "-Стоимость: "+ str(price)+ "$"

def strat1(action, country, from_date, to_date):
    from_date = from_date.replace('.', '/')
    to_date = to_date.replace('.', '/')
    df = investpy.get_stock_historical_data(stock=action,
                                            country=country,
                                            from_date=from_date,
                                            to_date=to_date)
    close = list(df['Close'].values)
    print(close)

    if close[-4] > close[-3] > close[-2] and close[-2] < close[-1]:
        return "покупаем 1 акцию"
    else:
        return "Держим"


def strat2(action, country, from_date, to_date):
    from_date = from_date.replace('.', '/')
    to_date = to_date.replace('.', '/')
    df = investpy.get_stock_historical_data(stock=action,
                                            country=country,
                                            from_date=from_date,
                                            to_date=to_date)
    close = list(df['Close'].values)
    if close[-4] < close[-3] < close[-2] and close[-2] > close[-1]:
        list_result = [close[-2], close[-1]]
        if (max(list_result) / min(list_result) - 1) * 100 >= 2:
            return "продаём 1 акцию"
        else:
            return "Держим"
    else:
        return "Держим"


def strat3(action, country, action_buy):
    if country == 'Russia':
        stock = action + '.ME'
    else:
        stock = action
    url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"

    querystring = {"symbol": stock, "region": country}

    headers = {
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
        "X-RapidAPI-Key": "7695aa1cd1mshc4c2550b8a4a75bp1c8a87jsn7818f71c796e"
    }
    action_buy = action_buy.replace(',','.')
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = response.text.split(',"')
    result_close_list = result[4].split(":")
    result_close = result_close_list[1]
    if float(result_close) < float(action_buy):
        list_result = [float(result_close), float(action_buy)]
        if (max(list_result) / min(list_result) - 1) * 100 >= 10:
            return "закрываем позицию"
        else:
            return "Держим"
    else:
        return "Держим"

def strat4(action, country, from_date, to_date, window1, window2):
    if country == 'Russia':
        stock = action + '.ME'
        tsla = yf.Ticker(stock)
    else:
        tsla = yf.Ticker(action)
    plt.rcParams['figure.figsize'] = (10, 5)
    plt.rcParams['axes.grid'] = True
    plt.rcParams["grid.linestyle"] = ":"
    plt.rcParams['lines.linewidth'] = 3

    from_date1 = from_date[-4:] + '-' + from_date[3:5] + '-' + from_date[0:2]
    to_date1 = to_date[-4:] + '-' + to_date[3:5] + '-' + to_date[0:2]

    tsla_history = tsla.history(start=from_date1, end=to_date1, interval="1d")
    print(tsla_history)

    tsla_history['ma_3'] = tsla_history['Close'].rolling(window=window1).mean()
    tsla_history['ma_10'] = tsla_history['Close'].rolling(window=window2).mean()

    plt.figure()
    plt.plot(tsla_history['Close'], label='close')
    plt.plot(tsla_history['ma_3'], label='ma_3')
    plt.plot(tsla_history['ma_10'], label='ma_10')
    plt.legend(['цена закрытия дня', f'средняя за {window1} дня', f'средняя за {window2} дней'], loc=2)

    plt.savefig('main/static/img1.jpg')

    tsla_history['position'] = (tsla_history['ma_3'] - tsla_history['ma_10']).apply(np.sign)
    tsla_history['log_return'] = tsla_history['Close'].apply(np.log).diff(1)
    tsla_history['my_log_return'] = tsla_history['position'].shift(1) * tsla_history['log_return']
    tsla_history['performance'] = tsla_history['my_log_return'].cumsum().apply(np.exp)

    if tsla_history['ma_3'][-1] > tsla_history['ma_10'][-1]:
        return f"покупаем"
    else:
        return f"продаём"


