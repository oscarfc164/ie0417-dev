'''
Devices module entry point
'''

from ..device import Device

from .computers import ComputerDevice


class DeviceFactory():

    """
    Factory creates the dic with devices description
    """

    def __init__(self) -> None:
        self._device_type_to_cls = {
            "computer": ComputerDevice
        }

    @property

    def supported_types(self):
        '''
        Returns list of names supported device types
        '''
        return[dtype for dtype in self._device_type_to_cls.keys()]

    def __call__(self, identificator: str, name: str, dtype: str, commands_s: list, ip_host: str) -> Device:
        """
        Creates the device

        :param str identificador: Identificator string
        :param str name: name of the device
        :param str dtype: device type
        :param list commands_s: list of commands supported by device
        :param str ip_host: ip addrees and host of device
        """
        device_cls = self._device_type_to_cls[dtype]
        return device_cls(identificator, name, commands_s, ip_host)
