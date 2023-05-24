from test_code.lcd_1602 import *

def close_door_hook():
    show_datetime()

def open_door_hook():
    show_datetime()

def show_datetime(): #「日時」を表示
    local_time = datetime.datetime.now()
    lcd_string(strftime("%Y.%m.%d (%a)", gmtime()) , LCD_LINE_1)
    lcd_string(local_time.strftime("%H:%M"), LCD_LINE_2)
    sleep(1)
