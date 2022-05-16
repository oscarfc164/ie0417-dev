from random import randint

from ..device import Device

class ComputerDevice(Device):
    def __init__(self, identificator: str, name: str, commands_s: list, host: str) -> None:
        super().__init__(identificator, name, commands_s, host)
