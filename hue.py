import os
import json
from typing import Dict

import requests

HUE_BRIDGE_IP_ADDRESS = "192.168.2.30"
LIGHT_ID_NAME = {
    "1": "Hue color lamp 1",
    "2": "Hue color lamp 2",
    "3": "Hue color lamp 3",
    "4": "Kotatsu 1",
    "5": "Kotatsu 3",
    "6": "Kotatsu 2",
    "7": "Entrance 1",
    "8": "Entrance 2",
    "9": "Entrance 3",
}

HUE_BRIDGE_USERNAME = os.environ['HUE_BRIDGE_USERNAME']
HUE_URL = "http://"+HUE_BRIDGE_IP_ADDRESS+"/api/"+HUE_BRIDGE_USERNAME+"/lights"


def turn_on_all_lights():
    update_all_light_state(True)


def turn_off_all_lights():
    update_all_light_state(False)
    

def get_light_status():
    response = requests.get(HUE_URL).json().items()
    light_id_state: Dict[str,bool] = {} 
    for id, val in response:
        light_id_state[id] = val['state']['on']
    print(type(light_id_state['1']))
    return light_id_state


def update_all_light_state(is_turn_on: bool):
    for id in LIGHT_ID_NAME.keys():
        light_url = HUE_URL + '/' + id + '/state'
        body = json.dumps({"on": is_turn_on})
        requests.put(light_url, data=body)


def main():
    get_light_status()


if __name__ == "__main__":
    main()
