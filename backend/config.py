import os
import logging
from environs import Env
from typing import Optional


def is_not_valid_config() -> None:
    env = Env()
    env.read_env()
    return env.bool("TEST_SKIP", True)


class Config:
    def __init__(self) -> None:
        self.env = Env()
        self.env.read_env()
        self.logging_level: Optional[int] = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        self.logging_level: int = logging.getLevelName(
            self.env.str("LOGGING_LEVEL", "INFO")
        )
        logging.basicConfig(
            level=self.logging_level,
            format="[%(asctime)s][%(levelname)s]:  %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def read_server_variables(self) -> None:
        self.port: int = self.env.int("PORT", 5000)
        self.host: str = self.env.str("HOST_IP", "127.0.0.1")
        self.debug: bool = self.env.bool("DEBUG", False)
        self.logger.debug("Server variables env loaded")

    def read_mongodb_variables(self) -> None:
        self.db_port: int = self.env.int("DB_PORT", 27017)
        self.db_host: str = self.env.str("DB_HOST_IP", "127.0.0.1")
        self.db_password: str = self.env.str("DB_PASSWORD", "")
        self.logger.debug("MongoDB variables env loaded")

    def read_hardware_variables(self) -> None:
        self.pir_sensor_channel: int = self.env.int("PIR_SENSOR_CHANNEL", 12)
        self.pir_debug_diode_channel: int = self.env.int("PIR_DEBUG_DIODE_CHANNEL", 40)
        self.camera_frame_width: int = self.env.int("CAMERA_FRAME_WIDTH", 1280)
        self.camera_frame_height: int = self.env.int("CAMERA_FRAME_HEIGHT", 720)
        self.servo_channel: int = self.env.int("SERVO_CHANNEL", 32)
        self.logger.debug("Hardware variables env loaded")

    def read_algorithm_variables(self) -> None:
        self.record_data_period: int = self.env.int("RECORD_DATA_PERIOD", 60)
        self.logger.debug("Algorithm variables env loaded")
