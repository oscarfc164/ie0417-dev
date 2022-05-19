import sys
import requests
import functools
import json.decoder
from pprint import pformat

def main():
    default_url = 'http://127.0.0.1:8000'
    sys_url = sys.argv[1] if (len(sys.argv) >= 2) else None

    url = sys_url or default_url

    wait_enter = functools.partial(input, "Hit Enter ")

    def pprint_response(resp):
        try:
            print(pformat(resp.json()), "\n")
        except json.decoder.JSONDecodeError as e:
            print(e)

    print("Prueba 1: Imprime todos los devices")
    wait_enter()
    resp = requests.get(f"{url}/devices/")
    pprint_response(resp)

    print("Prueba 3: Crea un nuevo device y imprime la lista")
    wait_enter()
    new_item = {
        "DEV3"
    }[
        {"name": "HP-Pavilon",
        "tipo": "Computer",
        "commands_s": ["read", "upload"],
        "ip_host": "127.0.0.1:5555"}]
    resp = requests.post(f"{url}/devices/", json=new_item)
    pprint_response(resp)

    print("Prueba 4: Obtiene un device especifico")
    wait_enter()
    resp = requests.get(f"{url}/items/DEV1")
    pprint_response(resp)

    print("Prueba 5: Elimina el device DEV2 e imprime resultado")
    wait_enter()
    resp = requests.delete(f"{url}/items/DEV2")
    pprint_response(resp)
