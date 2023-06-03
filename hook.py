import datetime
from time import sleep
from time import gmtime, strftime
import http.client
import os

from lib.lcd import lcd_string
import lib.lcd as lcd

def close_door_hook():
    show_datetime()

    # 以下 REMO経由でACを落とすコード
    conn = http.client.HTTPSConnection("api.nature.global")

    payload = "button=power-off"

    headers = {
      'accept': "application/json",
      'Content-Type': "application/x-www-form-urlencoded",
      'Authorization': "Bearer " + os.environ["REMO_TOKEN"]
    }

    conn.request("POST", "/1/appliances/19c992ee-1bf3-4270-89a3-5f86ab7b9ad7/aircon_settings", payload, headers)

    conn.getresponse()

def open_door_hook():
    show_datetime()

    # 以下 REMO経由でACをつけるコード
    conn = http.client.HTTPSConnection("api.nature.global")

    payload = "button=power-on"

    headers = {
      'accept': "application/json",
      'Content-Type': "application/x-www-form-urlencoded",
      'Authorization': "Bearer " + os.environ["REMO_TOKEN"]
    }

    conn.request("POST", "/1/appliances/19c992ee-1bf3-4270-89a3-5f86ab7b9ad7/aircon_settings", payload, headers)

    conn.getresponse()



def show_datetime(): #「日時」を表示
    local_time = datetime.datetime.now()
    lcd_string(strftime("%Y.%m.%d (%a)", gmtime()) , lcd.LCD_LINE_1)
    lcd_string(local_time.strftime("%H:%M"), lcd.LCD_LINE_2)
    sleep(1)
