from typing import List
from prometheus_client import start_http_server, Summary

IS_DOOR_OPEN = 0


def set_door_metrics(is_door_open: bool):
    IS_DOOR_OPEN.set(int(is_door_open))
    

def set_light_metrics(are_lights_on: List[bool]):
    for light_id, is_on in are_lights_on:
        pass


def start_prometheus_exporter():
    start_http_server(8000)
    IS_DOOR_OPEN = Summary(
        'is_door_open',  # name
        'whether door is open(=1) or close(=0)'  # description
    )
