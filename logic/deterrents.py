from abc import ABC, abstractmethod
import logging
import RPi.GPIO as GPIO
import time

logger = logging.getLogger(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class IDeterrent(ABC):
    @abstractmethod
    def deter(self) -> None:
        raise NotImplementedError


class ServoDeterrent(IDeterrent):
    def __init__(self, channel: int, pwm_frequency: int = 50) -> None:
        self.channel = channel
        GPIO.setup(self.channel, GPIO.OUT)
        self.servo = GPIO.PWM(self.channel, pwm_frequency)
        self.move()

    def deter(self) -> None:
        logger.info("Deterring by using moving object!")
        self.move(180)
        time.sleep(0.5)
        self.move(0)

    def move(self, angle: int = 0) -> None:
        self.servo.start(0)
        # Accept angle in range 0-180
        # TODO: Add info about mapping angle to duty value
        duty_cycle_value: float = 2 + (angle / 18)
        try:
            time.sleep(0.1)
            self.servo.ChangeDutyCycle(duty_cycle_value)
            time.sleep(0.5)
            self.servo.ChangeDutyCycle(0)
        finally:
            self.servo.stop()
            GPIO.cleanup()  # TODO: Check function and rebuild
