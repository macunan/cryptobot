#!/usr/bin/python3
import json
import math
import os
from binance.client import Client
import env
api_key=env.api_key
api_secret=env.api_secret
import config
from datetime import datetime

def buyprice():

 if not findstartupfile():
  return 0


 with open(config.loglocation+'lastoperation.json') as json_file:
     data = json.load(json_file)
 price=data['data'][0]['price']

 operation=data['data'][0]['operation']
 json_file.close
 if operation=='BUY':
  return float(price)
 else:return 0

def findstartupfile():
 fileName='lastoperation.json'
 PATH = config.loglocation
 for root, dirs, files in os.walk(PATH):
  for File in files:
    found = File.find(fileName)
    if found != -1:
     return True
  return False




def currentprice(tradingpair):
 while True:
  try:
   client = Client(api_key, api_secret)
   pinfo=client.get_all_tickers()
   break
  except:
   print("Error en currentprice")
  # except: continue
# Extract data in json format
 for x in pinfo:
    if x['symbol']==tradingpair:
        buyprice=x['price']
 return float(buyprice)


def startstatus():
 if not findstartupfile():
  return 'NONE',0


 with open(config.loglocation+'lastoperation.json') as json_file:
     data = json.load(json_file)
     # print(data['data'][0]['price'])
     # print(data['data'][0]['operation'])
 price=data['data'][0]['price']
 operation=data['data'][0]['operation']
 json_file.close
 return operation,price

# def findstartupfile():
# fileName='lastoperation.json'
# PATH = config.loglocation
# for root, dirs, files in os.walk(PATH):
# for File in files:
# found = File.find(fileName)
# if found != -1:
# return True
# return False


def createbuyorderusdt(tradingpair,amount):


 amount=float(amount)



 while True:
  try:
   client = Client(api_key, api_secret)
   orders = client.get_all_orders(symbol=tradingpair,limit=2)
   pinfo=client.get_all_tickers()
   balance = client.get_asset_balance(asset=config.buycoin)
   tradeinfo=client.get_symbol_info(tradingpair)
   break
  except:
   print("Error en createbuyorder1")



 for x in pinfo:
    if x['symbol']==tradingpair:
        buyprice=x['price']
#if amount left is less than amount create an order with cash that is left
 if float(balance['free']) < amount:
     amount=float(balance['free'])

 osize=truncate((amount/float(buyprice))*(1-0.1/100),int(dp(tradeinfo)))
 print(osize)

 while True:
  try:
    order = client.order_market_buy(
    symbol=tradingpair,
    quantity=osize)
    #order = client.order_market_buy(
    #symbol=tradingpair,
    #quantity=osize
    ##,price=buyprice
    #)
    break
  except:
     print("Error en createbuyorder2")

 print("all ok")
 print(order)
 buyprice=getboughtprice()

# datetime object containing current date and time
 now = datetime.now()
 

# dd/mm/YY H:M:S
 dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


 data = {}
 data['data'] = []
 data['data'].append({
    'price': buyprice,
    'operation': 'BUY',
    'coin':config.tradingpair,
    'date_time':dt_string
 })


 with open(config.loglocation+'lastoperation.json', 'w') as outfile:
  json.dump(data, outfile)

 data = {}
 data[dt_string] = []
 data[dt_string].append({
    'price': buyprice,
    'operation': 'BUY',
    'coin':config.tradingpair,
    'date_time':dt_string
 })
 with open(config.loglocation+'operations.json', 'a') as outfile:
  json.dump(data, outfile)
  outfile.write('\n')


 return buyprice



def createsellorderusdt(tradingpair):
 count=0
 while True:
  try:
   client = Client(api_key, api_secret)
   pinfo=client.get_all_tickers()
   balance = client.get_asset_balance(asset=config.sellcoin)
   tradeinfo=client.get_symbol_info(tradingpair)
   break
  # except: continue
  except:
   print("Error en creasellorder1")
 print(tradeinfo)
 for x in pinfo:
    if x['symbol']==tradingpair:
        sellprice=x['price']
        # sellamount=round(float(balance['free'])*(1-0.1/100),int(tradeinfo['baseAssetPrecision']-3))
        sellamount=truncate(float(balance['free']),int(dp(tradeinfo)))
        print("sellamount:"+str(sellamount))
 while True:

  if float(balance['free']) >=sellamount:
    try:
     order = client.order_market_sell(
     symbol=tradingpair,
     quantity=sellamount
     #,price=sellprice
     )
     print("order")
     print(order)
     break
    except:
        print("Error en creasellorder2 :"+str(truncate(sellamount,dp(tradeinfo))))
        sellamount=sellamount-0.00001
        sellamount=truncate(float(sellamount),int(dp(tradeinfo)))
        count=count+1
        if count==10:
         os.system(config.restartstring)
  else:
    sellamount=truncate(float(balance['free']),int(dp(tradeinfo)))
    try:
     order = client.order_market_sell(
     symbol=tradingpair,
     quantity=sellamount)
     print("order")
     print(order)
     break
    except:
      print("Error en creasellorderelse"+str(sellamount))

 now = datetime.now()
# dd/mm/YY H:M:S
 dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
 data = {}
 data['data'] = []
 data['data'].append({
    'price': sellprice,
    'operation': 'SELL',
    'coin':config.tradingpair,
    'date_time':dt_string
 })


 with open(config.loglocation+'lastoperation.json', 'w') as outfile:
  json.dump(data, outfile)
 data={}
 data[dt_string] = []
 data[dt_string].append({
    'price': sellprice,
    'operation': 'SELL',
    'coin':config.tradingpair,
    'date_time':dt_string
 })

 with open(config.loglocation+'operations.json', 'a') as outfile:
  json.dump(data, outfile)
  outfile.write('\n')

 return sellprice


# client = Client(api_key, api_secret)
# balance = client.get_asset_balance(asset='BTC')
# print(balance['free'])
# print(createbuyorderusdt('BTCUSDT',11))

#print(createbuyorderusdt('BTCUSDT',11))

# print(createsellorderusdt('BTCUSDT'))


def dp(tradeinfo):
 p=tradeinfo['filters']
 for x in p:
     if x['filterType']=='LOT_SIZE':
      print(x['stepSize'])
      if x['stepSize'].find('1') == 0:
       return 0
      else:
       return x['stepSize'].find('1')-1



def truncate(number, digits) -> float:
 stepper = 10.0 ** digits
 return math.trunc(stepper * number) / stepper
#gets average bought price for market order
def getboughtprice()->str:

 while True:
  try:
   client = Client(api_key, api_secret)
   orders = client.get_all_orders(symbol=config.tradingpair,limit=1)
   break
  except:
   print("Error in get getboughtprice")
  # except: continue
# Extract data in json format


 for x in orders:
      sellcoinamount=x['executedQty']
      buycoinamount=x['cummulativeQuoteQty']

 return  str(float(buycoinamount)/float(sellcoinamount))
    # if x['symbol']==tradingpair:
    #     sellprice=x['price']

 # print(orders['cummulativeQuoteQty'])
 # print(orders['cummulativeQuoteQty']/orders['executedQty'])


# print(truncate(0.00161490,6))

# print("ver si se encuentra archivo de inicio:")
# print(findstartupfile())
# print("testing boughtprice:")
# print(getboughtprice())
