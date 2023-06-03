import datetime
from time import sleep
from time import gmtime, strftime

from lib.lcd import lcd_string
import lib.lcd as lcd

from remo_api import aircon_on, aircon_off

def close_door_hook():
    show_datetime()

    aircon_off()

def open_door_hook():
    show_datetime()

    aircon_on()


def show_datetime(): #「日時」を表示
    local_time = datetime.datetime.now()
    lcd_string(strftime("%Y.%m.%d (%a)", gmtime()) , lcd.LCD_LINE_1)
    lcd_string(local_time.strftime("%H:%M"), lcd.LCD_LINE_2)
    sleep(1)
