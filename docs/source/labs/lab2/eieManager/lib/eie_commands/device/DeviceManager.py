import json
from typing import Optional, List, Dict

from numpy import dtype

from ..Command import Command
from .devices import DeviceFactory
from .device import Device


class DeviceManager:
    '''
    Manager class control for devices

    :param str config_filename: Name of the file with 
    devices info
    '''
    def __init__(self, config_filename: str) -> None:
        self.config_filename = config_filename
        self.init_config()
        self.device_factory = DeviceFactory()
        self.devices: Dict[str, Device] = {}
        self.device_per_type: Dict[str, Dict[str, Device]] = {}
    
    def _init_devices_per_type(self):
        '''
        Initializes a devices per-type mapping dictionary
        '''

        for device in self.devices.values():
            dtype = device.type()
            identificator = device.identificator()
            name = device.name()
            commands_s = device.commands_supported()
            ip_host = device.host()
            if dtype not in self.device_per_type:
                self.device_per_type[dtype] = {}
            self.device_per_type[dtype][name][identificator][commands_s][ip_host] = device

    def init_config(self) -> None:
        with open(self.config_filename) as config_file:
            devices_config = json.load(config_file)
            device_info = devices_config["devices"]
            for device_info in device_info:
                identificator = device_info["identificator"]
                name = device_info["name"]
                dtype = device_info["dtype"]
                commands_s = device_info["commands_s"]
                host = device_info["ip_host"]

        self._init_devices_per_type()

    def get_device_type(self) -> List[str]:
        '''
        Returns the list of device types
        '''
        return [name for name in self.device_per_type.keys()]

    def get_device_name_per_type(self, dtype: str) -> List[str]:
        '''
        Returns the list of device names for a device type
        '''
        names: List[str] = []
        type_devices = self.device_per_type.get(dtype)
        if type_devices is not None:
            names = [name for name in type_devices.keys()]
        return names

    