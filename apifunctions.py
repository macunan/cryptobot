#!/usr/bin/python3
import requests
import time
import binanceapi
import env
import config
tradingpair=config.sellcoin+'/'+config.buycoin
secretapi=env.secretapi
timeframe=config.timeframe
class FinanceApi:
 def ranginglogic(self):
# hma300=hullma(tradingpair,timeframe,300)
# macdema=macdext(tradingpair,timeframe)
# macema=macd(tradingpair,timeframe)
# bprice=binanceapi.buyprice()
# s=stochapi(tradingpair,timeframe)
# k=s['valueK']
# d=s['valueD']
# ma13=maapi(tradingpair,timeframe,13)
# if macdema['valueMACD']>macdema['valueMACDSignal']:
# if k>d and k<80 :
# if k>d and k<80 :
# and binanceapi.currentprice(config.sellcoin+config.buycoin) > hma300:
# return "BUY"
# if macdema['valueMACD']<= macdema['valueMACDSignal'] and  binanceapi.currentprice(config.sellcoin+config.buycoin) >= bprice*float(config.pp) :
# return "SELL"
  return "HOLD"





 def logicup(self):
  hullma50=self.hullma(tradingpair,timeframe,50)
  hullma13=self.hullma(tradingpair,timeframe,13)
  s=self.stochapi(tradingpair,timeframe)
  k=s['valueK']
  d=s['valueD']
  if k > d and k < 80  and (hullma13 >= hullma50) :
       return "BUY"
  bprice=binanceapi.buyprice()
  if k<=d  and  binanceapi.currentprice(config.sellcoin+config.buycoin) >= bprice*float(config.pp) :
       return "SELL"
  return "HOLD"

 def trend(self):
  hullma50=self.hullma(tradingpair,'1h',50)
  hullma13=self.hullma(tradingpair,'1h',13)
  if hullma13 > hullma50:
   return "UP"
  else:
    return "DOWN"


 def emaapi(self,symbol,interval,emavalue):
 # Define indicator
  indicator="ema"
# Define endpoint
  endpoint = f"https://api.taapi.io/{indicator}"

# Define a parameters dict for the parameters to be sent to the API
  parameters = {
'secret':secretapi,
'exchange':'binance',
'symbol':symbol,
'interval':interval,
'optInTimePeriod':emavalue
 }
  return self.generic(symbol,interval,indicator,parameters)


 def stochapi(self,symbol,interval):
 # Define indicator
  indicator="stochtv"
# Define endpoint
  endpoint = f"https://api.taapi.io/{indicator}"

# Define a parameters dict for the parameters to be sent to the API
  parameters = {
'secret':secretapi,
'exchange':'binance',
'symbol':symbol,
'interval':interval,
'kPeriod':'9',
'dPeriod':'3',
'kSmooth':'5'
  }

  return self.generic(symbol,interval,indicator,parameters)




 def macdext(self,symbol,interval):
 # Define indicator
  indicator="macdext"
# Define a parameters dict for the parameters to be sent to the API
  parameters = {
'secret':secretapi,
'exchange':'binance',
'symbol':symbol,
'interval':interval,
'optInFastPeriod':'8',
'optInSlowPeriod':'21',
'optInSignalPeriod':'5',
'optInFastMAType':'2',
'optInSlowMAType':'2',
'optInSignalMAType':'2'
}
  return self.generic(symbol,interval,indicator,parameters)



 def macd(self,symbol,interval):
 # Define indicator
  indicator="macdext"
# Define a parameters dict for the parameters to be sent to the API
  parameters = {
'secret':secretapi,
'exchange':'binance',
'symbol':symbol,
'interval':interval,
'optInFastPeriod':'20',
'optInSlowPeriod':'50',
'optInSignalPeriod':'13',
'optInFastMAType':'1',
'optInSlowMAType':'1',
'optInSignalMAType':'1'
}
  return self.generic(symbol,interval,indicator,parameters)


 def hullma(self,symbol,interval,period):
   # Define indicator
   indicator="hma"
   # Define endpoint
   parameters = {
   'secret':secretapi,
   'exchange':'binance',
   'symbol':symbol,
   'interval':interval,
   'period':period
     }
   return self.generic(symbol,interval,indicator,parameters)



 def maapi(self,symbol,interval,mavalue):
 # Define indicator
  indicator="ma"
# Define endpoint

# Define a parameters dict for the parameters to be sent to the API
  parameters = {
'secret':secretapi,
'exchange':'binance',
'symbol':symbol,
'interval':interval,
'optInTimePeriod':mavalue
}

  return self.generic(symbol,interval,indicator,parameters)


#Generic URL used for communications need to send symbol
#,interval,#incicator from taapio and parameters for that indicator
 def generic(self,symbol,interval,indicator,parameters):
# Define endpoint
  endpoint = f"https://api.taapi.io/{indicator}"
# Send get request and save the response as response object
  while True:
   try:
    response = requests.get(url = endpoint, params = parameters)
    result = response.json()
    if len(result) > 1:
      return(result)
    if len(result) == 1:
     if str(result['value']) != ' ':
      return(result['value'])
   except:
      time.sleep(10)
      continue
# Extract data in json format

# Print result




# print(logicup())
# p1=FinanceApi()
# print(p1.trend())
# print(macd('ETH/USDT',timeframe))
# print(macdext('ETH/USDT',timeframe))
# print(emaapi('ETH/USDT',timeframe,'20'))
# print(emaapi('BTC/USDT',timeframe,'200'))
# print(emaapi('BTC/USDT',timeframe,'50'))
# print(stochapi('ETH/USDT',timeframe))
# print(hullma('ETH/USDT',timeframe,50))
# print(maapi('ETH/USDT',timeframe,500))
