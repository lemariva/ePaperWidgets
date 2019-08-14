import sys
import os
from newsapi import NewsApiClient

sys.path.insert(0, os.path.realpath('./'))
from display.image_processing import UIProc

try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?"+e.reason)

WIDGET_WIDTH = 180
WIDGET_HEIGHT = 384

class NewsWidget:

    def __init__(self, language="en", api_key=None, sources="bbc-news, the-verge", query=None):
        if (api_key == None):
            raise ValueError('API key is missing')
        #_api = NewsApiClient(api_key="981ce4eb96694e14a9e9d323cb55224d")
        self._api = NewsApiClient(api_key=api_key)
        self._language = language
        self._sources = sources
        self._query = query

        self._width = WIDGET_WIDTH
        self._height = WIDGET_HEIGHT

        self._top_headlines = None
        self._news_feeds = []

    def get_data(self):
        print("Connecting to news API servers...")
        try:
            if (self._query == None):
                #_top_headlines = _api.get_top_headlines(sources="bbc-news", language="en")
                self._top_headlines = self._api.get_top_headlines(sources=self._sources,
                                                            language=self._language)
            else:
                self._top_headlines = self._api.get_top_headlines(q=self._query,
                                                            sources=self._sources,
                                                            language=self._language)
            self.__refresh_news__()
            self._data_available = True
        except Exception as e:
            """If no response was received from the openweathermap
            api server, add the cloud with question mark"""
            print('__________API-NEWS-ERROR!__________'+'\n')
            print('Reason: ',e,'\n')
            self._top_headlines = None
    
    def __refresh_news__(self):
        news_links = self._top_headlines['articles']

        for news in news_links:
            self._news_feeds.append(news)

    def get_widget_image(self):
        uiwriter = UIProc(self._language, self._width, self._height)
        h_line_size = 18
        
        news = []

        for news_feed in self._news_feeds:
            news.append(uiwriter.multiline_text(news_feed['title'], self._height))

        if len(news) > 6:
            del news[6:]
        
        idx = 0
        for lines in range(len(news)):
            idnew = True
            for line in news[lines]:
                if idnew:
                    uiwriter.write_text("# " + line, (0, h_line_size*idx))
                    idnew = False
                else:
                    uiwriter.write_text(line, (0, h_line_size*idx))
                idx = idx + 1

        return uiwriter.get_image()
