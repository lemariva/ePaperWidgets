import sys
import os

from coinbase.wallet.client import Client

sys.path.insert(0, os.path.realpath('./'))
from display.image_processing import UIProc


try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?"+e.reason)




class CoinWidget:

    def __init__(self, api_key = None, api_secret = None):
        if (api_key == None):
            raise ValueError('API key is missing')
            
        self.client = Client(api_key, api_secret)