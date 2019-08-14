import sys
import os

sys.path.insert(0, os.path.realpath('./'))
from display.image_processing import UIProc

try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?"+e.reason)   
    


class CalendarWidget:

    def __init__(self, week_starts_on):
        return

    @staticmethod
    def internet_available():
        try:
            urlopen('https://google.com',timeout=5)
            return True
        except URLError as err:
            return False