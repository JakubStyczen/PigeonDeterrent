from abc import ABC, abstractmethod
import logging
import RPi.GPIO as GPIO
from picamera import PiCamera
import picamera.array
import threading
import time
import numpy as np

from logic.utils.imageProcessing import gaussian_kernel, convolve

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

logger = logging.getLogger(__name__)


class IMotionSensor(ABC):
    @abstractmethod
    def is_motion_detected(self) -> bool:
        raise NotImplementedError


class PIRSensor(IMotionSensor):
    def __init__(self, channel: int, debug_diode_channel: int | None = None) -> None:
        self.channel = channel
        self.debug_diode_channel = debug_diode_channel
        GPIO.setup(self.channel, GPIO.IN)
        GPIO.setup(self.debug_diode_channel, GPIO.OUT)
        if self.debug_diode_channel is not None:
            threading.Thread(target=self.debug_diode_logic, daemon=True).start()

    def is_motion_detected(self) -> bool:
        return bool(GPIO.input(self.channel))

    def debug_diode_logic(self) -> None:
        try:
            while True:
                time.sleep(1)
                led_status = GPIO.HIGH if self.is_motion_detected() else GPIO.LOW
                GPIO.output(self.debug_diode_channel, led_status)
        finally:
            GPIO.output(self.debug_diode_channel, GPIO.LOW)


class CameraSensor(IMotionSensor):
    def __init__(self, frame_width: int = 1280, frame_height: int = 720) -> None:
        self.camera = PiCamera
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rotation = 180  # Default camera is upside down -> need rotation
        self.current_frame: picamera.array.PiRGBArray | None = self.capture()
        self.previous_frame: picamera.array.PiRGBArray | None = None

    def is_motion_detected(self) -> bool:
        time.sleep(0.5)
        return False

    def capture(self) -> np.array:
        with self.camera() as camera:
            camera.resolution = (self.frame_width, self.frame_height)
            camera.rotation = self.rotation
            with picamera.array.PiRGBArray(camera) as output:
                camera.capture(output, "rgb")
                return output.array

    def rgb2gray(self, frame: np.array) -> np.array:
        if frame is None or frame.size == 0:
            return np.array([])
        if frame is not None and isinstance(frame, np.ndarray):
            coefficients = np.array([0.299, 0.587, 0.114])
            grayscale_image = frame @ coefficients
            return np.round(grayscale_image).astype(np.uint8)

    def gaussian_blur(
        self, frame: np.array, kernel_size: int = 5, kernel_sigma: float = 1
    ) -> np.array:
        if frame is None or frame.size == 0:
            return np.array([])
        if frame is not None and isinstance(frame, np.ndarray):
            kernel = gaussian_kernel(kernel_size, kernel_sigma)
            return convolve(frame, kernel)
