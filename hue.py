import os
import json
from typing import Dict

import requests
from light_id_name import LIGHT_ID_NAME
from prometheus_exporter import set_light_metrics_on, set_light_metrics_off

HUE_BRIDGE_IP_ADDRESS = "192.168.2.30"

HUE_BRIDGE_USERNAME = os.environ['HUE_BRIDGE_USERNAME']
HUE_URL = "http://"+HUE_BRIDGE_IP_ADDRESS+"/api/"+HUE_BRIDGE_USERNAME+"/lights"


def turn_on_all_lights():
    update_all_light_state(True)
    set_light_metrics_on()


def turn_off_all_lights():
    update_all_light_state(False)
    set_light_metrics_off()


def get_light_status():
    response = requests.get(HUE_URL).json().items()
    light_id_state: Dict[str, bool] = {}
    for id, val in response:
        light_id_state[id] = val['state']['on']
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
