import json
from typing import Optional, List, Dict

from numpy import dtype

from .devices import DeviceFactory
from .device import Device


class DeviceManager:
    '''
    Manager class control for devices

    :param str config_filename: Name of the file with 
    devices info
    '''
    def __init__(self) -> None:
        self.init_config()
        self.device_factory = DeviceFactory()
        self.devices: Dict[Device] = {}
    

    def init_config(self) -> Dict:
        '''
        Initializes the devices from config and return
        the dict
        '''
        with open(self) as config_file:
            devices_config = json.load(config_file)
            device_info = devices_config["devices"]
            for device_info in device_info:
                identificator = device_info["identificator"]
                name = device_info["name"]
                dtype = device_info["dtype"]
                commands_s = device_info["commands_s"]
                host = device_info["ip_host"]
                self.devices[identificator] = self.device_factory(identificator, name, dtype, commands_s, host)
        return self.devices

    def add_device(
        self, 
        identificator: str,
        name: str,
        dtype: str,
        commands_s: list,
        ip_host: str
    ) -> Dict:
        '''
        Creates a new device and returns it as Dict
        '''
        new_device = {
            "identificator": identificator,
            "name": name,
            "dtype": dtype,
            "commands_s": commands_s,
            "ip_host": ip_host
        }
        self.devices[identificator] = self.device_factory(
            identificator, name, dtype, commands_s, ip_host
        )

        return self.devices
    
    def delete_device(self, identificador: str) -> Dict:
        """
        Delete a device and return the dict. 
        """
        for device in self.devices:
            if device == identificador:
                device.clear()

        return self.devices

    def send_command(self, command: str, identificator: str) -> str:
        '''
        Sends a command to a device and returns answer
        '''
        for device in self.devices:
            if device["identificador"] == identificator:
                lista_commands = device["commands_s"]
                if command in lista_commands:
                    return("Command accepted")
                else: 
                    return("Command denied")