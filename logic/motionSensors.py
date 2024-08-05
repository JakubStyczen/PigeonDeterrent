from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class IMotionSensor(ABC):
    @abstractmethod
    def is_motion_detect(self) -> None:
        raise NotImplementedError


class PIRSensor(IMotionSensor):
    def __init__(self) -> None:
        pass

    def is_motion_detect(self) -> None:
        raise NotImplementedError


class CameraSensor(IMotionSensor):
    def __init__(self) -> None:
        pass

    def is_motion_detect(self) -> None:
        raise NotImplementedError
