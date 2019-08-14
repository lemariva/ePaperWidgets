from PIL import Image, ImageDraw, ImageFont, ImageOps
import gc
from settings import *
import arrow
import numpy as np
from pytz import timezone

from display.calibration import calibration

from datetime import datetime, date, timedelta
from time import sleep
from dateutil.parser import parse

from display.e_paper_hw_drivers import EPD
from display.image_processing import UIProc

epd = EPD()

from widgets.Forecast import ForecastWidget
from widgets.News import NewsWidget
from widgets.Agenda import AgendaWidget

EPD_WIDTH = 640
EPD_HEIGHT = 384

'''Get system timezone and set timezone accordingly'''
with open('/etc/timezone','r') as file:
    lines = file.readlines()
    system_tz = lines[0].rstrip()
    local_tz = timezone(system_tz)

def main():
    """Create a blank white page first"""
    calibration_countdown = 'initial'

    forecast_widget = ForecastWidget(language, weather_api_key, units, hours, location)
    news_widget = NewsWidget(language, news_api_key)
    agenda_widget = AgendaWidget(calendarId=google_calendar_id)

    uiwriter = UIProc(language, EPD_WIDTH, EPD_HEIGHT)
    
    widget_grid = []
    widget_grid.append(forecast_widget)
    widget_grid.append(news_widget)
    widget_grid.append(agenda_widget)

    while True:
        time = datetime.now().replace(tzinfo=local_tz)
        hour = int(time.strftime("%-H"))
        month = int(time.now().strftime('%-m'))
        year = int(time.now().strftime('%Y'))
        mins = int(time.strftime("%M"))
        seconds = int(time.strftime("%S"))
        now = arrow.now(tz=system_tz)

        """At the hours specified in the settings file,
        calibrate the display to prevent ghosting"""
        if hour in calibration_hours:
            if calibration_countdown is 'initial':
                calibration_countdown = 0
                calibration()
            else:
                if calibration_countdown % (60 // int(update_interval)) is 0:
                    calibration()
                    calibration_countdown = 0

        """Refreshing widgets
        """
        y_position = 0
        for widget in widget_grid:
            widget.get_data()
            tmp_widget_img = widget.get_widget_image()
            uiwriter.paste_img(tmp_widget_img, (0, y_position))
            y_position = y_position + widget._width

        #forecast_widget.get_data()
        #forecast_img = forecast_widget.get_widget_image()   
        #uiwriter.paste_img(forecast_img)

        #news_widget.get_data()
        #news_img = news_widget.get_widget_image()
        #uiwriter.paste_img(news_img)

        #agenda_widget.get_data()
        #agenda_img = agenda_widget.get_widget_image()
        #uiwriter.paste_img(agenda_img)
          
        """
        Map all pixels of the generated image to red, white and black
        so that the image can be displayed 'correctly' on the E-Paper
        """
        buffer = np.array(uiwriter._image)
        r,g,b = buffer[:,:,0], buffer[:,:,1], buffer[:,:,2]
        if display_colours is "bwr":
            buffer[np.logical_and(r > 245, g > 245)] = [255,255,255] #white
            buffer[np.logical_and(r > 245, g < 245)] = [255,0,0] #red
            buffer[np.logical_and(r != 255, r == g )] = [0,0,0] #black

        if display_colours is "bw":
            buffer[np.logical_and(r > 245, g > 245)] = [255,255,255] #white
            buffer[g < 255] = [0,0,0] #black


        improved_image = Image.fromarray(buffer).rotate(270, expand=True)
        print('Initialising E-Paper Display')
        epd.init()
        sleep(5)
        print('Converting image to data and sending it to the display')
        epd.display_frame(epd.get_frame_buffer(improved_image))
        print('Data sent successfully')
        print('______Powering off the E-Paper until the next loop______'+'\n')
        epd.sleep()


        if calibration_countdown is 'initial':
            calibration_countdown = 0
        calibration_countdown += 1


if __name__ == '__main__':
    main()
