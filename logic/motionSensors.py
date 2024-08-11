from abc import ABC, abstractmethod
import logging
import RPi.GPIO as GPIO
from picamera import PiCamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

logger = logging.getLogger(__name__)


class IMotionSensor(ABC):
    @abstractmethod
    def is_motion_detect(self) -> bool:
        raise NotImplementedError


class PIRSensor(IMotionSensor):
    def __init__(self, channel: int) -> None:
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN)

    def is_motion_detect(self) -> bool:
        return bool(GPIO.input(self.channel))


class CameraSensor(IMotionSensor):
    def __init__(self) -> None:
        self.camera = PiCamera()
        self.camera.rotation = 180  # Default camera is upside down -> need rotation

    def is_motion_detect(self) -> bool:
        raise NotImplementedError
