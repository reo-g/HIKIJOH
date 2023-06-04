from typing import List, Dict
from prometheus_client import start_http_server, Summary, Enum, Gauge
from light_id_name import LIGHT_ID_NAME

OPEN_STATE = "open"
CLOSED_STATE = "closed"

ON_STATE = "on"
OFF_STATE = "off"

# initialize metrics
IS_DOOR_OPEN = Enum("is_door_open","hogehoge",states=[OPEN_STATE, CLOSED_STATE])
IS_LIGHT_ON = []
AIRCON_TEMP = Gauge("aircon_temp","fugafuga")
# IS_DOOR_OPEN = 0
# IS_LIGHT_ON = {}
# AIRCON_TEMP = 0




def set_aircon_metrics(aircon_state: Dict[str, str]):
    global AIRCON_TEMP
    print(aircon_state)
    print(aircon_state['temp'])
    AIRCON_TEMP.set(float(aircon_state['temp']))


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
            states=[ON_STATE, OFF_STATE]
        )
    AIRCON_TEMP = Gauge(
        'aircon_temperature',  # name
        'temperature of air conditioner'  # description
    )



def set_door_metrics_open():
    global IS_DOOR_OPEN
    IS_DOOR_OPEN.state(OPEN_STATE)


def set_door_metrics_closed():
    global IS_DOOR_OPEN
    IS_DOOR_OPEN.state(CLOSED_STATE)

# before
# def set_light_metrics_ons():
#     global IS_DOOR_OPEN, AIRCON_TEMP, IS_LIGHT_ON
#     for light_id, is_on in are_lights_on:
#         IS_LIGHT_ON[light_id].state(int(is_on))

# after
def set_light_metrics_on():
    global IS_LIGHT_ON
    for light_id, _ in LIGHT_ID_NAME:
        IS_LIGHT_ON[light_id].state(ON_STATE)


def set_light_metrics_off():
    global IS_LIGHT_ON
    for light_id, _ in LIGHT_ID_NAME:
        IS_LIGHT_ON[light_id].state(OFF_STATE)
