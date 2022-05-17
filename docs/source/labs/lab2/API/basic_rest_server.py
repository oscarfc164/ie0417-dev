"""
REST API using FASTAPI for eieManager
"""

from ntpath import join
from unicodedata import name
from fastapi import FastAPI, Body
from random import randint
from typing import Optional
from pydantic import BaseModel
import json


class Device(BaseModel):
    identificator: str
    name: str
    type_device: str
    commands_s : list
    host_port: str

app = FastAPI()


with open("devices.json") as filename:
    devices = json.load(filename)



@app.post("/devices/", status_code= 201)
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
    


@app.delete("/devices/{identificator}")
def delete_item(identificador: str, status_code=204):
    """
    Unregister and delete item.
    :param str device_name: Name of the device to delete.
    :param int status_code: Default HTTP status code to return.
    """
    devices.pop(identificador)
    return devices

@app.get("/devices/{identificator}")
def read_item(identificator: str):
    """
    Get specific device from identificator.
    :param str item_name: Name of the device to get.
    """
    device = devices[identificator]
    return device
