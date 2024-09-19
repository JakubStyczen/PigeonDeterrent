from abc import ABC, abstractmethod
import logging
import RPi.GPIO as GPIO
from picamera import PiCamera
import picamera.array
import threading
import time
import numpy as np

from logic.utils.imageProcessing import gaussian_kernel, convolve

logger = logging.getLogger(__name__)

THRESHOLD = 30

DETECTION_DIFF_THRESHOLD = 14 * 200 * 200 * 255


class IMotionSensor(ABC):
    @abstractmethod
    def is_motion_detected(self) -> bool:
        raise NotImplementedError


class PIRSensor(IMotionSensor):
    def __init__(self, channel: int, debug_diode_channel: int | None = None) -> None:
        # Setup GPIO conf
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.channel = channel
        self.debug_diode_channel = debug_diode_channel
        GPIO.setup(self.channel, GPIO.IN)
        if self.debug_diode_channel is not None:
            logger.info("Started debug diode mode for PIR sensor in thread")
            GPIO.setup(self.debug_diode_channel, GPIO.OUT)
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
        self.current_frame: np.array = self._init_frame()
        self.previous_frame: np.array | None = None
        logger.debug("init")

    def _init_frame(self) -> np.array:
        init_frame = self.capture()
        # return self.gaussian_blur(self.rgb2gray(init_frame))
        return self.rgb2gray(init_frame)

    def is_motion_detected(
        self, threshold_diff: int = DETECTION_DIFF_THRESHOLD
    ) -> bool:
        new_frame = self.capture()
        self.previous_frame = self.current_frame
        self.current_frame = self.rgb2gray(new_frame)
        # self.current_frame = self.gaussian_blur(self.rgb2gray(new_frame))

        frame_diff = np.abs(self.previous_frame - self.current_frame)

        thresholded_diff = self.thresholding(frame_diff)

        thresholded_diff_sum = thresholded_diff.sum()

        if thresholded_diff_sum > DETECTION_DIFF_THRESHOLD:
            logger.debug(f"Frame threshold sum: {thresholded_diff_sum}")
            return True
        return False

    def capture(self) -> np.array:
        with self.camera() as camera:
            camera.resolution = (self.frame_width, self.frame_height)
            camera.rotation = self.rotation
            with picamera.array.PiRGBArray(camera) as output:
                camera.capture(output, "rgb")
                return output.array

    @staticmethod
    def rgb2gray(frame: np.array) -> np.array:
        if frame is None or frame.size == 0:
            return np.array([])
        if frame is not None and isinstance(frame, np.ndarray):
            coefficients = np.array([0.299, 0.587, 0.114])
            grayscale_image = frame @ coefficients
            return np.round(grayscale_image).astype(np.uint8)

    @staticmethod
    def gaussian_blur(
        frame: np.array, kernel_size: int = 5, kernel_sigma: float = 1
    ) -> np.array:
        if frame is None or frame.size == 0:
            return np.array([])
        if frame is not None and isinstance(frame, np.ndarray):
            kernel = gaussian_kernel(kernel_size, kernel_sigma)
            return convolve(frame, kernel)

    @staticmethod
    def thresholding(frame_diff: np.array, threshold: int = THRESHOLD) -> np.array:
        return np.where(frame_diff >= threshold, 255, 0)
