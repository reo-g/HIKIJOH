import pigpio
import time

class Switch:
    #set switch PIN
    switch_pin = 4

    def __init__(self):
        self.pi = pigpio.pi()

        pi.set_mode(switch_pin, pigpio.INPUT)
        pi.set_pull_up_down(switch_pin, pigpio.PUD_UP)

    def switch_status(self):
        if self.pi.read(switch_pin) == 1:
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
