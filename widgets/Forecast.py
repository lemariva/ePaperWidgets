import sys
import os
import pyowm
import arrow
import time
from pytz import timezone
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.realpath('./'))
from display.image_processing import UIProc
from display.image_data import *

try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?"+e.reason)

'''Get system timezone and set timezone accordingly'''
with open('/etc/timezone','r') as file:
    lines = file.readlines()
    system_tz = lines[0].rstrip()
    local_tz = timezone(system_tz)

WIDGET_WIDTH = 190
WIDGET_HEIGHT = 384

class ForecastWidget:

    def __init__(self, language, api_key, units, hours, location):
        if (api_key is None or ""):
            raise ValueError('API key is missing')

        self._owm = pyowm.OWM(api_key, language=language)
        self._location = location
        self._units = units
        self._hours = hours
        self._forecast_data = []
        self._language = language

        self._now = arrow.now(tz=system_tz)

        self._width = WIDGET_WIDTH
        self._height = WIDGET_HEIGHT

        self._daily_forecast_data = []
        self._actual_data = {}
        #self._forecast_data = []

    def get_data(self):
        print("Connecting to Openweathermap API servers...")
        if self._owm.is_API_online() is True:
            try:
                self._three_hours_forecast = self._owm.three_hours_forecast(self._location)
                self._actual_observation =  self._owm.weather_at_place(self._location)
                self._daily_forecast = self._owm.daily_forecast(self._location)

                self.__refresh_weather__()
                self.__refresh_horly_forecast__()
                self.__refresh_daily_forecast__()

            except Exception as e:
                """If no response was received from the openweathermap
                api server, add the cloud with question mark"""
                print('__________OWM-ERROR!__________'+'\n')
                print('Reason: ',e,'\n')
        else:
            raise ValueError('Openweathermap not available')

    def __refresh_weather__(self):
        #location = self._actual_observation.get_location().get_name()
        weather = self._actual_observation.get_weather()
        timestamp = weather.get_reference_time()

        weather_icon = weather.get_weather_icon_name()     
        humidity = str(weather.get_humidity())
        #cloudstatus = str(weather.get_clouds())
        weather_description = str(weather.get_detailed_status())

        if self._units is "metric":
            temperature = str(int(weather.get_temperature(unit='celsius')['temp']))
            wind_speed = str(int(weather.get_wind()['speed']))

            
        if self._units is "imperial":
            temperature = str(int(weather.get_temperature('fahrenheit')['temp']))
            wind_speed = str(int(weather.get_wind()['speed']*0.621))
            

        sunrise_time = arrow.get(weather.get_sunrise_time()).to(system_tz)
        sunset_time = arrow.get(weather.get_sunset_time()).to(system_tz)

        self._actual_data = {'time': timestamp,
                            'temperature': temperature,
                            'humidity': humidity,
                            'windspeed': wind_speed,
                            'icon': weather_icon,
                            'description': weather_description,
                            'sunrise': sunrise_time,
                            'sunset': sunset_time}

    
    def __refresh_daily_forecast__(self):
        forecasts = self._daily_forecast.get_forecast().get_weathers()
        self._daily_forecast_data = []

        for forecast in forecasts:
            timestamp = forecast.get_reference_time()
            weather_icon = forecast.get_weather_icon_name()   
            humidity = forecast.get_humidity()
            weather_description = str(forecast.get_detailed_status())

            if self._units is "metric":
                temp_max = str(int(forecast.get_temperature(unit='celsius')['max']))
                temp_min = str(int(forecast.get_temperature(unit='celsius')['min']))
                wind_speed = str(int(forecast.get_wind()['speed']))
                
            if self._units is "imperial":
                temperature = str(int(forecast.get_temperature('fahrenheit')))
                temp_max = str(int(forecast.get_temperature(unit='fahrenheit')['max']))
                temp_min = str(int(forecast.get_temperature(unit='fahrenheit')['min']))
                wind_speed = str(int(forecast.get_wind()['speed']*0.621))
            
            forecast_struct = {'time': timestamp,
                            'tmax': temp_max,
                            'tmin': temp_min,
                            'humidity': humidity,
                            'windspeed': wind_speed,
                            'icon': weather_icon,
                            'description': weather_description}

            self._daily_forecast_data.append(forecast_struct)

    
    def __refresh_horly_forecast__(self):
        forecasts = self._three_hours_forecast.get_forecast().get_weathers()
        self._forecast_data = []

        for forecast in forecasts:
            timestamp = forecast.get_reference_time()
            weather_icon = forecast.get_weather_icon_name()   
            humidity = forecast.get_humidity()
            weather_description = str(forecast.get_detailed_status())

            if self._units is "metric":
                temperature = str(int(forecast.get_temperature(unit='celsius')['temp']))
                wind_speed = str(int(forecast.get_wind()['speed']))
                
            if self._units is "imperial":
                temperature = str(int(forecast.get_temperature('fahrenheit')['temp']))
                wind_speed = str(int(forecast.get_wind()['speed']*0.621))
            
            forecast_struct = {'time': timestamp,
                            'temperature': temperature,
                            'humidity': humidity,
                            'windspeed': wind_speed,
                            'icon': weather_icon,
                            'description': weather_description}
            self._forecast_data.append(forecast_struct)


    def get_widget_image(self):
        uiwriter = UIProc(self._language, self._width, self._height)
        h_line_size = 18

        # actual weather

        uiwriter.draw_rectangle((0,0), (150, 80))
        uiwriter.write_text(weathericons[self._actual_data['icon']], (5,1), font_type = "w_font_l", colour="red")
        uiwriter.write_text(self._actual_data['description'], (60, 1))

        if self._hours is "24":
            uiwriter.write_text(self._actual_data['sunrise'].format('H:mm'), (60, h_line_size))
        if self._hours is "12":
            uiwriter.write_text(self._actual_data['sunrise'].format('h:mm'), (60, h_line_size))

        sunsettime = self._actual_data['sunset']
        sunrisetime = self._actual_data['sunrise']

        if (self._now <= sunrisetime and self._now <= sunsettime) or (self._now >= sunrisetime and self._now >= sunsettime):
            #uiwriter.write_text('\uf051', (60, h_line_size), font_type = "w_font_ss")
            if self._hours is "24":
                uiwriter.write_text(sunrisetime.format('H:mm'), (95, h_line_size))
            if self._hours is "12":
                uiwriter.write_text(sunrisetime.format('h:mm'), (95, h_line_size))

        if self._now >= sunrisetime and self._now <= sunsettime:
            #uiwriter.write_text('\uf052', (50, h_line_size), font_type = "w_font_ss")
            if self._hours is "24":
                uiwriter.write_text(sunsettime.format('H:mm'), (95, h_line_size))
            if self._hours is "12":
                uiwriter.write_text(sunsettime.format('h:mm'), (95, h_line_size))

        uiwriter.write_text(self._actual_data['humidity'] + " %", (95, h_line_size*2))
        if self._units is "metric":
            uiwriter.write_text(self._actual_data['temperature'] + " °C", (60, h_line_size*2))
            uiwriter.write_text(self._actual_data['windspeed'] + " km/h", (60, h_line_size*3))

        if self._units is "imperial":
            uiwriter.write_text(self._actual_data['temperature'] + " °F", (60, h_line_size*2))
            uiwriter.write_text(self._actual_data['windspeed'] + " mph", (60, h_line_size*3))

        ## horly forecast
        idx = 0
        for ff in self._forecast_data[0:4]:
            uiwriter.write_text(time.strftime("%H:%M", time.localtime(ff['time'])), (155, 1 + (idx)*h_line_size))
            uiwriter.write_text(weathericons[ff['icon']], (195, 1 + (idx)*h_line_size), font_type = "w_font_ss", colour="red")
            uiwriter.write_text(ff['temperature'] + " °", (220, 1 + (idx)*h_line_size))
            uiwriter.write_text(ff['description'], (260, 1 + (idx)*h_line_size))
            idx = idx + 1


        ## daily forecast
        idx = 0
        for ff in self._daily_forecast_data[0:5]:
            uiwriter.draw_rectangle(((idx)*78, 85), (70, 90))
            uiwriter.write_text(weathericons[ff['icon']], ((idx)*78+10, 86), font_type = "w_font_l", colour="red")
            uiwriter.write_text(time.strftime("%d.%m", time.localtime(ff['time'])), ((idx)*78+15, 136))
            

            if self._units is "metric":
                uiwriter.write_text(ff['tmax'] + " °C", ((idx)*78+25, 151))
                uiwriter.write_text(ff['tmin'] + " - ", ((idx)*78+2, 151))
                
            if self._units is "imperial":
                uiwriter.write_text(ff['tmax'] + " °F", ((idx)*78+25, 151))
                uiwriter.write_text(ff['tmin'] + " - ", ((idx)*78+2, 151))
            
            idx = idx + 1

        return uiwriter.get_image()