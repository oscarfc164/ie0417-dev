'''
Devices module entry point
'''

from zmq import device
from ..device import *




class DeviceFactory():

    """
    Factory creates the dic with devices description
    """

    def __init__(self) -> None:
        self.devices = {
            "identificator": Device.identificator(),
            "name": Device.name(),
            "dtype": Device.type(),
            "commands_s": Device.commands_supported(),
            "ip_host": Device.host()
        }

