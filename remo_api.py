import http.client
import os
import json

from prometheus_exporter import set_aircon_metrics

def aircon_on():
    # 以下 REMO経由でACをつけるコード
    conn = http.client.HTTPSConnection("api.nature.global")

    payload = "button=power-on"

    headers = {
      'accept': "application/json",
      'Content-Type': "application/x-www-form-urlencoded",
      'Authorization': "Bearer " + os.environ["REMO_TOKEN"]
    }

    conn.request("POST", "/1/appliances/19c992ee-1bf3-4270-89a3-5f86ab7b9ad7/aircon_settings", payload, headers)

    # conn.getresponse()
    response = conn.getresponse()
    aircon_state = json.loads(response.read().decode())
    set_aircon_metrics(aircon_state)
    return aircon_state

def aircon_off():

# 以下 REMO経由でACを落とすコード
    conn = http.client.HTTPSConnection("api.nature.global")

    payload = "button=power-off"

    headers = {
      'accept': "application/json",
      'Content-Type': "application/x-www-form-urlencoded",
      'Authorization': "Bearer " + os.environ["REMO_TOKEN"]
    }

    conn.request("POST", "/1/appliances/19c992ee-1bf3-4270-89a3-5f86ab7b9ad7/aircon_settings", payload, headers)

    # conn.getresponse()
    response = conn.getresponse()
    aircon_state = json.loads(response.read().decode())
    set_aircon_metrics(aircon_state)
    return aircon_state
  
if __name__ == "__main__":
    aircon_off()

