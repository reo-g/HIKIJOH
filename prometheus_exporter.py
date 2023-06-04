from typing import List, Dict
from prometheus_client import start_http_server, Summary, Enum
from hue import LIGHT_ID_NAME

# initialize metrics
IS_DOOR_OPEN:int = 0
IS_LIGHT_ON:Dict[str,int] = {}
AIRCON_TEMP:int = 0

OPEN_STATE = "open"
CLOSED_STATE = "closed"

ON_STATE = "on"
OFF_STATE = "off"

def set_door_metrics_open():
    IS_DOOR_OPEN.state(OPEN_STATE)

def set_door_metrics_closed():
    IS_DOOR_OPEN.state(CLOSED_STATE)

def set_light_metrics_ons
    for light_id, is_on in are_lights_on:
        IS_LIGHT_ON[light_id].state(int(is_on))

def set_aircon_metrics(aircon_state: Dict[str,str]):
    AIRCON_TEMP.set(int(aircon_state['temp']))
    

def start_prometheus_exporter():
    global IS_DOOR_OPEN, AIRCON_TEMP, IS_LIGHT_ON
    start_http_server(8000)
    IS_DOOR_OPEN = Enum(
        'is_door_open',  # name
        'whether door is open or closed',  # description
        states=[OPEN_STATE, CLOSED_STATE]
    )
    for light_id, name in LIGHT_ID_NAME.items():
        IS_LIGHT_ON[light_id] = Enum(
            'is_' + name.replace(" ", "_") + '_on',  # name
            'whether light is on(=1) or off(=0)',  # description
            states=[OFF_STATE, ON_STATE]
        )
    AIRCON_TEMP = Summary(
        'aircon_temperature',  # name
        'temperature of air conditioner'  # description
    )
