from abc import ABC, abstractmethod
import logging

from deterrents import IDeterrent, ServoDeterrent
from motionSensors import IMotionSensor, PIRSensor, CameraSensor

logger = logging.getLogger(__name__)


class IMotionDetectionAlgorithm(ABC):
    pass


class MotionDetectionAlgorit(IMotionDetectionAlgorithm):
    pass
