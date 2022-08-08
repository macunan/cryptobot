#!/usr/bin/python3
import apifunctions
import binanceapi
import logging
import time
import config
from datetime import datetime
initflag=True
bottrend=False
datestr = "%m/%d/%Y %I:%M:%S %p "
logging.basicConfig(
            filename=config.loglocation+"botexecution.log",
            level=logging.WARNING,
            filemode="w",
            datefmt=datestr,
)
p1=apifunctions.FinanceApi()
#bot gets amount to buy from config file
usdtamount=config.amount
#bot gets bought price and botmode from startup file if none present botmode will be BUY thanks to If below
botmode,bprice=binanceapi.startstatus()

print("initial botmode value:"+botmode)
print(len(botmode))


if botmode == 'SELL' and initflag:
    botmode="BUY"
    initflag=False



if botmode == 'BUY' and initflag:
    print("in botmode Buy initial if")
    botmode='SELL'
    print("New value of botmode :"+botmode)
    initflag=False


if botmode == 'NONE' and initflag:
    botmode='INITIAL'
    initflag=False

#once we enter the While we never come out
while True:
 logging.warning("Aca trend function:")
 print("Aca trend function:")
 print(p1.trend())
 logging.warning(p1.trend())
 logging.warning("Found init file")
 print(binanceapi.findstartupfile())
 logging.warning(binanceapi.findstartupfile())
 print("Current bot from api functions status:"+str(p1.logicup()))
 logging.warning("Current bot from api functions status:"+str(p1.logicup()))
 print("Current bot from botmode variable: "+botmode)
 logging.warning("Current bot from botmode variable: "+str(botmode))
 logging.warning("Current Price "+str(binanceapi.currentprice(config.sellcoin+config.buycoin)))
 # exit()

 if p1.trend()=='RANGING':
  bottrend=True
  #bot buys in uptrend since all indicators give green and botmode is in buy
  if  p1.ranginglogic()=='BUY' and botmode == 'BUY':
    binanceapi.createbuyorderusdt(config.tradingpair,usdtamount)
    botmode='SELL'
    print("bot is buying in rangingtrend")
    logging.warning("bot is buying ranging trend")
  if  p1.ranginglogic()=='SELL' and botmode == 'SELL':
    binanceapi.createsellorderusdt(config.tradingpair)
    botmode='BUY'
    print("bot is selling in rangingtrend")
    logging.warning("bot is selling in rangingtrend")
 
 if p1.trend()=='UP':
  bottrend=True
  #bot buys in uptrend since all indicators give green and botmode is in buy
  if  p1.logicup()=='BUY' and botmode == 'BUY':
    binanceapi.createbuyorderusdt(config.tradingpair,usdtamount)
    botmode='SELL'
    print("bot is buying in uptrend")
    logging.warning("bot is buying uptrend")
# bot sells since in anytrend and all indicators and botmode give go ahead of sale
 if  p1.logicup() == 'SELL' and botmode == 'SELL':
   binanceapi.createsellorderusdt(config.tradingpair)
   botmode='BUY'
   print("bot is selling")
   logging.warning("bot is selling")

# bot sells when 50ema crosses below 200ema and bot has bought  this is like stoploss and config.stoploss is True right now is false is good idea to set this to true in really large timaframes like daily.
 if  p1.trend()=='DOWN' and botmode == 'SELL' and bottrend and config.stoploss:
    binanceapi.createsellorderusdt(config.tradingpair)
    print("bot is selling  stoploss")
    logging.warning("bot is selling due to stoploss")
    botmode='BUY'
    bottrend=False
 if p1.trend()=='DOWN':
  bottrend=False
 if botmode=='INITIAL' and p1.logicup()=='SELL':
  botmode='BUY'


 print("bot will wait "+str(config.checktime)+" seconds and start next iteration")
 logging.warning("bot will wait "+str(config.checktime)+" seconds and start next iteration")
 print("Curent date and time: "+str(datetime.now()))
 logging.warning("Curent date and time: "+str(datetime.now()))
 time.sleep(config.checktime)
