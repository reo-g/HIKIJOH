from typing import List, Dict
from prometheus_client import start_http_server, Summary, Enum, Gauge
from hue import LIGHT_ID_NAME

# initialize metrics
IS_DOOR_OPEN:str = ""
IS_LIGHT_ON:Dict[str,str] = {}
AIRCON_TEMP:str = ""

OPEN_STATE = "open"
CLOSED_STATE = "closed"

ON_STATE = "on"
OFF_STATE = "off"

def set_door_metrics_open():
    IS_DOOR_OPEN.state(OPEN_STATE)

def set_door_metrics_closed():
    IS_DOOR_OPEN.state(CLOSED_STATE)

# def set_light_metrics_ons():
#     global IS_DOOR_OPEN, AIRCON_TEMP, IS_LIGHT_ON
#     for light_id, is_on in are_lights_on:
#         IS_LIGHT_ON[light_id].state(int(is_on))

def set_aircon_metrics(aircon_state: Dict[str,str]):
    global IS_DOOR_OPEN, AIRCON_TEMP, IS_LIGHT_ON
    AIRCON_TEMP.set_to_current_time()
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
            'whether light is on or off',  # description
            states=[OFF_STATE, ON_STATE]
        )
    AIRCON_TEMP = Gauge(
        'aircon_temperature',  # name
        'temperature of air conditioner'  # description   
    )
    
