import logging

from app import App
from config import Config
from logic.deterrents import ServoDeterrent
from logic.motionSensors import PIRSensor, CameraSensor
from logic.motionAlgorithm import MotionDetectionAlgoritm

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Config()
    config.read_server_variables()
    config.read_mongodb_variables()
    config.read_hardware_variables()

    servo_detterent = ServoDeterrent(config.servo_channel)
    pir_sensor = PIRSensor(config.pir_sensor_channel)
    camera_sensor = CameraSensor(config.camera_frame_width, config.camera_frame_height)

    motion_algorithm = MotionDetectionAlgoritm(
        db, [pir_sensor, camera_sensor], [servo_detterent]
    )

    app = App(config.host, config.port, config.debug)
    app.run()
