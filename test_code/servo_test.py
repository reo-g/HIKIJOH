#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio
import time

pi = pigpio.pi()

pi.set_servo_pulsewidth(18, 700)
time.sleep(0.1)
pi.set_servo_pulsewidth(18, 0)
time.sleep(3)

pi.set_servo_pulsewidth(18, 2300)
time.sleep(0.1)
pi.set_servo_pulsewidth(18, 0)
time.sleep(3)