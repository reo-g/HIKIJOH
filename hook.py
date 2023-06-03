import datetime
from time import sleep
from time import gmtime, strftime

from lib.lcd import lcd_string
import lib.lcd as lcd

from hue import turn_on_all_lights, turn_off_all_lights

def close_door_hook():
    turn_off_all_lights()

def open_door_hook():
    turn_on_all_lights()

def show_datetime(): #「日時」を表示
    local_time = datetime.datetime.now()
    lcd_string(strftime("%Y.%m.%d (%a)", gmtime()) , lcd.LCD_LINE_1)
    lcd_string(local_time.strftime("%H:%M"), lcd.LCD_LINE_2)
    sleep(1)
