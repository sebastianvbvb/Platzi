
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, date,  timedelta
import matplotlib.pyplot as plt
import requests
import time
import subprocess
#from scipy.interpolate import make_interp_spline


currencies = ['USD', 'CZK', 'ARS']
exchange_api_key = 'P9MFWMVMFB6MQJQO'
exchange_rates = pd.DataFrame()
for i in currencies:
    url  = f'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol={i}&apikey={exchange_api_key}'
    r = requests.get(url)
    data = (r.json())["Time Series FX (Monthly)"]
    data = pd.DataFrame(data).transpose().reset_index()
    data.rename(columns= {'index' : 'month_year', '1. open' : 'open', '2. high' : 'high', '3. low' :'low', '4. close' :'close' }, inplace= True)
    data['avg'] = data.apply(lambda x:avg_rate(x.high, x.close), axis= 1)
    data['currency'] = i
    data['month_year'] = data.month_year.map(string_to_date)
    data['month_year'] = data.month_year.map(date_to_monthyear)
    exchange_rates = pd.concat([exchange_rates, data]).reset_index(drop=True)
    time.sleep(2)
