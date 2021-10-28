import pigpio
import time

class Switch:
    #set switch PIN
    switch_pin = 27

    def __init__(self):
        self.pi = pigpio.pi()

        self.pi.set_mode(Switch.switch_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(Switch.switch_pin, pigpio.PUD_UP)

    def switch_status(self):
        if self.pi.read(Switch.switch_pin) == 0:
            return True
        else:
            return False

def main():
    switch = Switch()

    while True:
        if switch.switch_status():
            print("スイッチが押されている")
        else:
            pass
        time.sleep(0.10)


if __name__ == '__main__':
    main()
