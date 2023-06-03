import os
import json

import requests

HUE_BRIDGE_IP_ADDRESS = "192.168.2.30"
LIGHT_ID_NAMES = {
    "1": "Hue color lamp 1",
    "2": "Hue color lamp 2",
    "3": "Hue color lamp 3",
    "4": "Kotatsu 1",
    "5": "Kotatsu 2",
    "6": "Kotatsu 3",
    "7": "玄関1",
    "8": "玄関2",
    "9": "玄関3",
}

HUE_BRIDGE_USERNAME = os.environ['HUE_BRIDGE_USERNAME']
HUE_URL = "http://"+HUE_BRIDGE_IP_ADDRESS+"/api/"+HUE_BRIDGE_USERNAME+"/lights"

def turn_on_all_lights():
    update_all_light_state(True)
    
def turn_off_all_lights():
    update_all_light_state(False)
    
def update_all_light_state(is_turn_on:bool):
    for id in LIGHT_ID_NAMES.keys():
        light_url = HUE_URL + '/' + id + '/state'
        body      = json.dumps({"on":is_turn_on})
        requests.put(light_url, data=body)
        
def main():
    turn_on_all_lights()
    
if __name__ == "__main__":
    main()
