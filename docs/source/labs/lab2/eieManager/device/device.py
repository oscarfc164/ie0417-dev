from typing import Optional
from abc import ABC, abstractmethod
from unicodedata import name

from numpy import dtype

from ..Command import Command

class Device(ABC):
    '''
    Device representation 

    :param str name: Name of the sensor
    :param str dtype: Type of the device
    :param str host: IP and host of device 
    '''

    def __init__(self, name: str, dtype: str, host: str) -> None:
        self._name = name
        self._dtype = dtype
        self._host = host

    def name(self) -> str:
        '''
        Gets the name of the device
        '''
        return self._name

    def type(self) -> str:
        """
        Gets the type of device
        """
        return self._dtype

    def host(self) -> str:
        '''
        Gets the ip and host of device
        '''
        return self._host

    @abstractmethod 
    def read(self) -> float:
        '''
        Reads the device an return it read
        '''
        pass

class DeviceReadCommand(Command):

    def __init__(
        self,
        device: Device,
    ) -> None:
        self.device = device

    def execute(self) -> None:

        name = self.device.name()
        dtype = self.device.type()
        host = self.device.host()
        value = self.device.read()

        print(f"DeviceReadCommand : [{dtype}] {name}: {value} {host}")

