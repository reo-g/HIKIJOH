# -*- coding: utf-8 -*-

import binascii
import nfc
import pigpio
from time import sleep
import time
import datetime
import smbus
import pandas as pd
import datetime

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address 
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


### LCD control

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  sleep(E_DELAY)
  

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


class Servo:
    #set servo PIN
    servo_pin = 18
    #set switch PIN
    switch_pin = 4

    def __init__(self):
        self.pi = pigpio.pi()

        self.pi.set_mode(Servo.switch_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(Servo.switch_pin, pigpio.PUD_UP)

    def switch_status(self):
        if self.pi.read(Servo.switch_pin) == 0:
            return True
        else:
            return False

    # 鍵を開ける
    def door_open(self):
        self.pi.set_servo_pulsewidth(Servo.servo_pin, 500)
        sleep(0.2)
        # 開放
        self.pi.set_servo_pulsewidth(Servo.servo_pin, 0)

    # 鍵を締める
    def door_close(self):
        self.pi.set_servo_pulsewidth(Servo.servo_pin, 2500)
        sleep(0.2)
        # 開放
        self.pi.set_servo_pulsewidth(Servo.servo_pin, 0)


class NFC_CARD:
    def __init__(self):
        ### NFC
        self.clf = nfc.ContactlessFrontend('usb')
        # 212F(FeliCa)
        self.target_suica = nfc.clf.RemoteTarget("212F")
        # 0003(Suica)
        self.target_suica.sensf_req = bytearray.fromhex("0000030000")
        # 212F(FeliCa) 学生証用に2つ起動させておく(suica以外のカード)
        self.target_req = nfc.clf.RemoteTarget("212F")

    def nfc_process(self):
        target = None
        target_res = self.clf.sense(target_suica, iterations=10, interval=0.01)
        target_res2 = self.clf.sense(target_req, iterations=1, interval=0.01)
        if target_res is not None:
            target = target_res
        elif target_res2 is not None:
            target = target_res2
        if target is not None:
            tag = nfc.tag.activate(self.clf,target)
            tag.sys = 3
            idm = binascii.hexlify(tag.idm)
            stridm = str(idm, 'utf-8')
            return stridm
        else:
            return None

class NFC_Data:
    def __init__(self):
        self.df = pd.read_csv('data/idm.csv')
    def check_registered(self,idm):
        if (self.df["idm"] == idm).sum() == 0: #登録されていなかったら
            return False
        else: #登録されていたら
            return True
    def registering_card(self,idm):
        self.df=self.df.append({'registered_date':datetime.date.today(),'idm':idm} , ignore_index=True)
        self.df.to_csv('data/idm.csv')



def main():
    door_isopen = True
    want_close = False
    card_istouch = False

    card = NFC_CARD()
    servo = Servo()
    nfc_data = NFC_Data()

    lcd_init()
    servo.door_open() ##最初は開けておく
    
    lcd_string("   Welcome to   ", LCD_LINE_1)
    lcd_string(" CAMPHOR- LOCK ", LCD_LINE_2)

    sleep(2) #LCDを2秒間点灯
    LCD_BACKLIGHT = 0x00  #バックライトオフ
    lcd_byte(0x01, LCD_CMD) #表示内容クリア

    while True:
        ret = card.nfc_process()
        if ret is not None:
            card_istouch = True
            card_touched_time = time.time()
            LCD_BACKLIGHT  = 0x08  # On
            is_timeout = False:

            if nfc_data.check_registered(ret): #idmがすでに登録されているカードだったら
                lcd_string("   Welcome to   ", LCD_LINE_1)
                lcd_string(" CAMPHOR- HOUSE ", LCD_LINE_2)
                if want_close == True and door_isopen == True:
                    servo.door_close()
                    door_isopen = False
                    want_close = False

                if want_close == False and door_isopen == False:
                    servo.door_open()
                    door_isopen = True
                    
            else: #登録されていないカードだったら
                lcd_string("  THIS CARD IS  ", LCD_LINE_1)
                lcd_string(" NOT REGISTERED ", LCD_LINE_2)
                while True: #5秒間ボタン入力を受け付ける
                    if servo.switch_status(): #ボタンの入力がされたら
                        lcd_string(" PLEASE TOUCH  ", LCD_LINE_1)
                        lcd_string(" REGISTERED CARD", LCD_LINE_2)
                        wait_master_time = time.time()

                        while True: #すでに登録されたカードのタッチを15秒待つ
                            ret_m = card.nfc_process()
                            if time.time() - wait_master_time > 15:
                                is_timeout = True
                                lcd_string("REGISTERATION IS", LCD_LINE_1)
                                lcd_string(" TIMEOUT... >_< ", LCD_LINE_2)
                                break
                            if ret_m is not None:
                                if nfc_data.check_registered(ret_m): #idmがすでに登録されているカードだったら
                                    nfc_data.registering_card(ret) #元々タッチされたカードを追加する
                                    lcd_string(" THIS CARD IS  ", LCD_LINE_1)
                                    lcd_string("REGISTERED! ^o^ ", LCD_LINE_2)
                                    is_timeout = True #ループから抜けるために便宜上
                                    break
                                else:
                                    lcd_string(" THIS CARD IS  ", LCD_LINE_1)
                                    lcd_string(" NOT MASTER CARD ", LCD_LINE_2)
  
                    if time.time() - card_touched_time > 5:
                        is_timeout = True
                    
                    if is_timeout == True:
                        is_timeout = False
                        break
        if card_istouch == True:
            if time.time() - card_touched_time > 60:
                #LCDの焼け付きを防止するために消す
                card_istouch = False
                LCD_BACKLIGHT = 0x00  #バックライトオフ
                lcd_byte(0x01, LCD_CMD) #表示内容クリア

        if servo.switch_status():
            if want_close != True:
                lcd_string("HOUSE CLOSE MODE", LCD_LINE_1)
                lcd_string(" TOUCH KEY ^o^ ", LCD_LINE_2)
                want_close_time = time.time()
                want_close = True

        if want_close == True:
            if time.time() - want_close_time > 60:
                #LCDの焼け付きを防止するために消す
                want_close = False
                LCD_BACKLIGHT = 0x00  #バックライトオフ
                lcd_byte(0x01, LCD_CMD) #表示内容クリア    



if __name__ == '__main__':
    main()