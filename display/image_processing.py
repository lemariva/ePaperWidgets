from PIL import Image, ImageDraw, ImageFont, ImageOps
from display.image_data import *

w_font_l = ImageFont.truetype(fpath+weather_font, 40)
w_font_s = ImageFont.truetype(fpath+weather_font, 22)
w_font_ss = ImageFont.truetype(fpath+weather_font, 14)

class UIProc:
    def __init__(self, language, width, height, font_size=14):
        if language in ['ja','zh','zh_tw','ko']:
            self._default = ImageFont.truetype(fpath+NotoSansCJK+'Light.otf', font_size)
            self._semi = ImageFont.truetype(fpath+NotoSansCJK+'DemiLight.otf', font_size)
            self._bold = ImageFont.truetype(fpath+NotoSansCJK+'Regular.otf', font_size)
            self._month_font = ImageFont.truetype(fpath+NotoSansCJK+'DemiLight.otf', 40)
        else:
            self._default = ImageFont.truetype(fpath+NotoSans+'Light.ttf', font_size)
            self._semi = ImageFont.truetype(fpath+NotoSans+'.ttf', font_size)
            self._bold = ImageFont.truetype(fpath+NotoSans+'Medium.ttf', font_size)
            self._month_font = ImageFont.truetype(fpath+NotoSans+'Light.ttf', 40)
        
        self._width = width
        self._height = height
        self._image = Image.new('RGB', (height, width), 'white')
    
    def clean_img(self):
        self._image = Image.new('RGB', (self._height, self._width), 'white')

    def paste_img(self, space, position_xy=(0, 0)):
        self._image.paste(space, position_xy)

    def get_image(self):
        return self._image

    """Custom function to display a rectangle on the E-Paper"""
    def draw_rectangle(self, start, stop, line_width=2, colour="black"):
        x = start[0]
        size_x = stop[0]
        y = start[1]
        size_y = stop[1]
        space = Image.new('RGB', (size_x, size_y), color='white')
        ImageDraw.Draw(space).rectangle(((0, 0), (int(size_x), int(size_y))), fill=colour)
        ImageDraw.Draw(space).rectangle(((line_width-1, line_width-1), (int(size_x)-line_width, int(size_y)-line_width)), fill="white")
        
        self._image.paste(space, (int(x),int(y)))

    """Custom function to display text on the E-Paper"""
    def write_text(self, text, tuple_xy = None, font_type="default", alignment='left', colour='black'):
        font = self._default
        
        if font_type=="semi":
            font = self._semi
        elif font_type=="bold":
            font = self._bold
        elif font_type=="month_font": 
            font = self._month_font
        elif font_type=="w_font_l":
            font = w_font_l
        elif font_type=="w_font_s":
            font = w_font_s
        elif font_type=="w_font_ss":
            font = w_font_ss

        text_width, text_height = font.getsize(text)

        while (text_width, text_height) > (self._height, self._width):
            text=text[0:-1]
            text_width, text_height = font.getsize(text)

        if tuple_xy is None:
            if alignment is "middle":
                x = int((self._width / 2) - (text_width / 2))
            elif alignment is "" or alignment is 'left' or None:
                x = 0
            y = 0
        else:
            x = tuple_xy[0]
            y = tuple_xy[1]
            
        space = Image.new('RGB', (text_width, int(text_height * 1.1)), color='white')
        ImageDraw.Draw(space).text((0, 0), text, fill=colour, font=font)

        self._image.paste(space, (int(x),int(y)))

    """Custom function to display longer text into multiple lines (wrapping)"""
    def multiline_text(self, text, max_width, font_type="default"):
        font = self._default
        
        if font_type=="semi":
            font = self._semi
        elif font_type=="bold":
            font = self._bold
        elif font_type=="month_font": 
            font = self._month_font
        elif font_type=="w_font_l":
            font = w_font_l
        elif font_type=="w_font_s":
            font = w_font_s
        elif font_type=="w_font_ss":
            font = w_font_ss

        lines = []
        if font.getsize(text)[0] <= max_width:
            lines.append(text)
        else:
            words = text.split(' ')
            i = 0
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)

        return lines