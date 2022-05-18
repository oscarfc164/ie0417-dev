"""
REST API using FASTAPI for eieManager
"""

from ntpath import join
from click import command
from fastapi import FastAPI, Body
from random import randint
from typing import Optional
from pydantic import BaseModel
from device.manager import DeviceManager



app = FastAPI()

@app.get("/devices/")
def read_devices():
   DeviceManager.__init__()


