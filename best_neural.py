import logging
import time
from threading import Thread
import json
import numpy as np
import pandas as pd
from datetime import datetime
from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.common import OrderId, ListOfContractDescription, BarData,\
        HistogramDataList, TickerId
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.utils import iswrapper

def best_neutral(probs, chain, spreads):
    profits = []
    max_profit = -1000.0
    max_index = -1
    for i, spread in enumerate(spreads):
        # Strike prices and premiums
        K1 = spread[0]
        K2 = spread[1]
        P1 = chain[K1]['P']['ask_price']
        P2 = chain[K2]['C']['ask_price']

        # Iterate through probabilities
        profit = 0.0
        for belief in probs:
            if belief < K1:
                profit += ((K1 - belief) - (P1 + P2)) * probs[belief]/(P1 + P2)
            elif belief > K2:
                profit += ((belief - K2) - (P1 + P2)) * probs[belief]/(P1 + P2)
            else:
                profit += -(P1 + P2) * probs[belief]/(P1 + P2)

        # Check for spread with maximum profit
        profits.append(profit)
        if profit > max_profit:
            max_profit = profit
            max_index = i
    return max_profit, max_index
