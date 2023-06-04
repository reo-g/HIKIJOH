from typing import List, Dict
from prometheus_client import start_http_server, Summary
from hue import LIGHT_ID_NAME

# initialize metrics
IS_DOOR_OPEN:int = 0
IS_LIGHT_ON:Dict[str,int] = {}
AIRCON_TEMP:int = 0

def set_door_metrics(is_door_open: bool):
    IS_DOOR_OPEN.set(int(is_door_open))
    

def set_light_metrics(are_lights_on: List[bool]):
    for light_id, is_on in are_lights_on:
        IS_LIGHT_ON[light_id].set(int(is_on))

def set_aircon_metrics(aircon_state: Dict[str,str]):
    AIRCON_TEMP.set(int(aircon_state['temp']))
    

def start_prometheus_exporter():
    start_http_server(8000)
    IS_DOOR_OPEN = Summary(
        'is_door_open',  # name
        'whether door is open(=1) or close(=0)'  # description
    )
    for light_id, name in LIGHT_ID_NAME:
        IS_LIGHT_ON[light_id] = Summary(
            'is_' + name + '_on',  # name
            'whether light is on(=1) or off(=0)'  # description
        )
    AIRCON_TEMP = Summary(
        'aircon_temperature',  # name
        'temperature of air conditioner'  # description
    )
    
