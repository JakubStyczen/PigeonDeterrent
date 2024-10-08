import logging
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import time

from backend.db.dbHandler import MongoDBHandler, IDBHandler

from logic.deterrents import ServoDeterrent
from logic.motionSensors import PIRSensor, CameraSensor
from logic.motionAlgorithm import MotionDetectionAlgoritm

if TYPE_CHECKING:
    from config import Config

logger = logging.getLogger(__name__)


class IController(ABC):

    @abstractmethod
    def get_db_handler(self) -> IDBHandler:
        raise NotImplementedError


class Controller(IController):
    def __init__(self, config: "Config") -> None:
        self.config = config
        # self.servo_detterent = ServoDeterrent(config.servo_channel)
        # self.pir_sensor = PIRSensor(config.pir_sensor_channel)
        # self.camera_sensor = CameraSensor(
        #     config.camera_frame_width, config.camera_frame_height
        # )
        self.mdb_handler = MongoDBHandler(ip=config.db_host, port=config.db_port)
        # self.motion_algorithm = MotionDetectionAlgoritm(
        #     self.mdb_handler,
        #     [self.pir_sensor, self.camera_sensor],
        #     [self.servo_detterent],
        #     config.record_data_period,
        # )

    def get_db_handler(self) -> MongoDBHandler:
        return self.mdb_handler

    def start_logic(self) -> None:
        logger.info("Starting main logic")
        self.mdb_handler.create_db_collection()
        # self.motion_algorithm.start_detecting()
        # self.motion_algorithm.start_recording()

    def stop_and_cleanup(self) -> None:
        logger.info("Stopping main logic")
        # self.motion_algorithm.stop_detecting()
        # self.motion_algorithm.stop_recording()
        self.mdb_handler.disconnect()
        # self.servo_detterent.cleanup()
        GPIO.cleanup()
