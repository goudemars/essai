import os.path
import time
import logging
from threading import Thread
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.common import OrderId, ListOfContractDescription, BarData,\
        HistogramDataList, TickerId
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.utils import iswrapper

class TestApp(EWrapper,EClient):
    def __init__(self, addr, port, client_id):
        EWrapper.__init__(self)
        EClient. __init__(self, self)
        # Connect to TWS
        self.connect(addr, port, client_id)
        # Launch the client thread
        thread = Thread(target=self.run)
        thread.start()

    def error(self, reqId, errorCode,errorString):
        print("Errror: ",reqId, " ", errorCode," ",errorString)

    def historicalData(self,reqId,bar):
        print("HistoricalData ",reqId," Date:",bar.date,"Open:", bar.open)


def main():
    
    app=TestApp('127.0.0.1',7497,0)

    contract=Contract()
    contract.symbol="EUR"
    contract.secType="CASH"
    contract.exchange="IDEALPRO"
    contract.currency="USD"

    app.reqHistoricalData(1,contract,"","1 D","1 min","MIDPOINT",0,1,False,[])

    app.run()

if __name__=="__main__":
    main()
    
