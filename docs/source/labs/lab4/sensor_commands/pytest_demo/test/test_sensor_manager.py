from pytest import fixture
from utils import rand_gen

@fixture
def sensor_mgr(example_mod_fixt, example_func_fixt):
    logging.info("Fixture 1 setup!")
    logging.info(f"example_mod_fixt: {example_mod_fixt}")
    logging.info(f"example_func_fixt: {example_func_fixt}")
    ctx = DemoFixtureContext()
    return ctx


def test_sensor_manager_supported_types():
    get_supported_sensor_stypes


def test_sensor_manager_single_sensor_create_destroy():
    create_sensor
    get_sensor_info

    destroy_sensor


def test_sensor_manager_single_sensor_read_command():
    create_sensor
    destroy_sensor




    class MockSensor:
    def __init__(self, name: str, stype: str, unit: str) -> None:
        self._name = name
        self._type = stype
        self._unit = unit

    def name(self) -> str:
        """
        Gets the name of the sensor.
        """
        return self._name

    def type(self) -> str:
        """
        Gets the type of the sensor.
        """
        return self._type

    def unit(self) -> str:
        """
        Gets the unit of the sensor.
        """
        return self._unit

    def test_sensor_manager_mock_type_register_unregister():
    
    
    def test_sensor_manager_mock_sensor_create_destroy():


    def test_sensor_manager_mock_sensor_read_command():
    
    
    
    @abstractmethod
    def read(self) -> float:
        """
        Reads the sensor.
        :return: Sensor reading.
        """
        pass


class SensorAnalyzer(ABC):
    """
    Generic sensor analyzer that processes updates from sensor reads.
    """
    @abstractmethod
    def update(self, value: float):
        """
        Updates the analyzer state with a new sensor reading.
        :param float value: Sensor reading value.
        """
        pass


class SensorReadCommand(Command):
    """
    Command to read a Sensor and optionally update a SensorAnalyzer.
    :param sensor: Sensor object.
    :type sensor: :class:`Sensor`
    :param analyzer: SensorAnalyzer object or None.
    :type analyzer: :class:`SensorAnalyzer` or None.
    """
    def __init__(
            self,
            sensor: Sensor,
            analyzer: Optional[SensorAnalyzer] = None
    ) -> None:
        self.sensor = sensor
        self.analyzer = analyzer

    def execute(self) -> None:
        """
        Reads the sensor and optionally send value to analyzer.
        """
        name = self.sensor.name()
        stype = self.sensor.type()
        unit = self.sensor.unit()
        value = self.sensor.read()
        if self.analyzer is not None:
            self.analyzer.update(value)
        print(f"SensorReadCommand: [{stype}] {name}: {value} {unit}")