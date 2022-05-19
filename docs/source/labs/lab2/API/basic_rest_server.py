"""
REST API using FASTAPI for eieManager
"""

from ntpath import join
from fastapi import FastAPI, Body
from random import randint
from typing import Optional
from pydantic import BaseModel
import json


class Device(BaseModel):
    name: str
    type_device: Optional[str] = None
    host_port: str

app = FastAPI()

devices_desc = []
with open('devices.json') as file:
    dev = json.load(file)

    for devs in dev['devices']:
        lista = (devs['name'], devs['tipo'])

        devices_desc.append(lista)

devices = {
    name: Device(
        name=name,
        tipo=tipo,
        host_port = "127.0.0.1" + ":" + str(randint(0000,9999))
    )
    for name, tipo in devices_desc
}



@app.post("/devices/")
def create_device(device: Device):
    """
    Create a new item and register it

    :param device, new device to register.
    """
    devices[device.name] = device
    return device


@app.get("/devices/")
def read_devices(first: int = 0, limit: int = 10):
    """
    Get a list of the current items.

    :param int first: First list element to get (optional).
    :param int limit: Maximum number of elements to get (optional).
    """
    devices_list = [device for device in devices.values()]
    return devices_list[first : first + limit]


@app.delete("/devices/{device_name}")
def delete_item(device_name: str, status_code=204):
    """
    Unregister and delete item.

    :param str device_name: Name of the device to delete.
    :param int status_code: Default HTTP status code to return.
    """
    del devices[device_name]


@app.get("/devices/{device_name}")
def read_item(device_name: str):
    """
    Get specific device from name.

    :param str item_name: Name of the device to get.
    """
    return devices[device_name]
