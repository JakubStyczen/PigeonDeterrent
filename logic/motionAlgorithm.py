from abc import ABC, abstractmethod
import logging
import time
import schedule
from datetime import datetime
from collections import namedtuple
import threading

from logic.deterrents import IDeterrent
from logic.motionSensors import IMotionSensor
from backend.db.dbHandler import IDBHandler

logger = logging.getLogger(__name__)

AlgorithmData = namedtuple(
    "AlgorithmData", "time_of_motion_captuted, sensors_interrupt_dict"
)


class IMotionDetectionAlgorithm(ABC):
    def __init__(
        self,
        db_handler: IDBHandler,
        sensors_list: list[IMotionSensor],
        deterrents_list: list[IDeterrent],
        record_data_period: int,
    ) -> None:
        self.db_handler = db_handler
        self.sensors_list = sensors_list
        self.deterrents_list = deterrents_list
        self.record_data_period = record_data_period
        self.is_alarm_triggered: bool = False
        self.is_data_recorded: bool = True
        self.time_of_motion_captuted: datetime = datetime.now()
        self.sensors_interrupt_dict: str[str, bool] = {
            sensor.__class__.__name__: sensor.is_motion_detected()
            for sensor in self.sensors_list
        }

    def start_recording(self) -> None:
        logger.info("Data recording has been started")
        self.is_data_recorded = True

    def stop_recording(self) -> None:
        logger.info("Data recording has been stopped")
        self.is_data_recorded = False

    def get_algorithm_data(self) -> AlgorithmData:
        return AlgorithmData(self.time_of_motion_captuted, self.sensors_interrupt_dict)

    @abstractmethod
    def start_detecting(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop_detecting(self) -> None:
        raise NotImplementedError


class MotionDetectionAlgoritm(IMotionDetectionAlgorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_thread_running = True
        self.lock = threading.RLock()

        schedule.every(self.record_data_period).seconds.do(self.capture_data)

    def start_recording(self) -> None:
        super().start_recording()
        threading.Thread(target=self.recording_wrapper, daemon=True).start()

    def recording_wrapper(self) -> None:
        while self.is_data_recorded:
            schedule.run_pending()
            time.sleep(1)

    def capture_data(self) -> None:
        with self.lock:
            self.db_handler.create_record(
                self.time_of_motion_captuted, self.sensors_interrupt_dict
            )
        logger.debug(f"Data has been recorded")

    def stop_recording(self) -> None:
        logger.info("Data recording has been stopped")
        with self.lock:
            self.is_data_recorded = False

    def update_is_motion_detected(self) -> None:
        sensors_state_list: dict[str, bool] = {
            sensor.__class__.__name__: sensor.is_motion_detected()
            for sensor in self.sensors_list
        }
        if any(sensors_state_list.values()):
            self.is_alarm_triggered = True
            self.time_of_motion_captuted = datetime.now()
            self.sensors_interrupt_dict = sensors_state_list
            return
        self.is_alarm_triggered = False

    def detection_alogrithm(self) -> None:
        while self.is_thread_running:
            self.update_is_motion_detected()
            logger.debug(
                f"Motion detection status: {self.time_of_motion_captuted=}, {self.sensors_interrupt_dict=}"
            )
            if self.is_alarm_triggered:
                for deterrent in self.deterrents_list:
                    deterrent.deter()
                time.sleep(5)
                self.is_alarm_triggered = False
            time.sleep(2)

    def start_detecting(self) -> None:
        self.is_thread_running = True
        logger.info("Motion detection has been started")
        threading.Thread(target=self.detection_alogrithm, daemon=True).start()

    def stop_detecting(self) -> None:
        logger.info("Motion detection has been stopped")
        with self.lock:
            self.is_thread_running = False
