import pytest
import time
import sys
import numpy as np

from logic.motionSensors import PIRSensor, CameraSensor
from backend.config import is_not_valid_config


@pytest.mark.skipif(is_not_valid_config(), reason="Skip tests which requires hardware")
class TestPIRSensor:
    def test_debug_diode_logic(self):
        pir_sensor = PIRSensor(12, 40)
        pir_sensor.debug_diode_logic()
        pass


@pytest.fixture
def camera_sensor():
    return CameraSensor()


@pytest.mark.skipif(is_not_valid_config(), reason="Skip tests which requires hardware")
class TestCameraSensor:

    def test_capture_default_frame_size(self, camera_sensor):
        frame = camera_sensor.capture()
        assert frame.shape == (720, 1280, 3)

    def test_capture_custom_frame_size(self):
        camera_sensor = CameraSensor(640, 480)
        frame = camera_sensor.capture()
        assert frame.shape == (480, 640, 3)

    def test_rgb2gray(self, camera_sensor):
        # Test case 1: Test conversion of RGB image to grayscale
        frame = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
        gray_frame = camera_sensor.rgb2gray(frame)
        assert np.array_equal(gray_frame, np.array([76, 150, 29]))

        # Test case 2: Test conversion of empty image
        frame = np.array([])
        gray_frame = camera_sensor.rgb2gray(frame)
        assert np.array_equal(gray_frame, np.array([]))

    def test_gaussian_blur_default_kernel(self, camera_sensor):
        # Test case: Test Gaussian blur with default kernel size and sigma
        frame = np.array(
            [
                [0.1622, 0.6020, 0.4505, 0.8258, 0.1067],
                [0.7943, 0.2630, 0.0838, 0.5383, 0.9619],
                [0.3112, 0.6541, 0.2290, 0.9961, 0.0046],
                [0.5285, 0.6892, 0.9133, 0.0782, 0.7749],
                [0.1656, 0.7482, 0.1524, 0.4427, 0.8173],
            ]
        )
        blurred_frame = camera_sensor.gaussian_blur(frame, 3)
        expected_frame = np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0.40460013, 0.43169432, 0.52443752, 0],
                [0, 0.49263108, 0.49243327, 0.51401432, 0],
                [0, 0.55740066, 0.54215183, 0.49360314, 0],
                [0, 0, 0, 0, 0],
            ]
        )

        assert np.allclose(blurred_frame, expected_frame)

    def test_gaussian_blur_custom_kernel(self, camera_sensor):
        # Test case: Test Gaussian blur with custom kernel size and sigma
        frame = np.array(
            [
                [0.8687, 0.4314, 0.1361, 0.8530, 0.0760],
                [0.0844, 0.9106, 0.8693, 0.6221, 0.2399],
                [0.3998, 0.1818, 0.5797, 0.3510, 0.1233],
                [0.2599, 0.2638, 0.5499, 0.5132, 0.1839],
                [0.8001, 0.1455, 0.1450, 0.4018, 0.2400],
            ]
        )

        kernel_size = 3
        kernel_sigma = 0.5
        blurred_frame = camera_sensor.gaussian_blur(frame, kernel_size, kernel_sigma)
        expected_frame = np.array(
            [
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0,
                    0.71782357,
                    0.74748037,
                    0.58956772,
                    0,
                ],
                [
                    0,
                    0.3131408,
                    0.54885178,
                    0.39238271,
                    0,
                ],
                [
                    0,
                    0.28052706,
                    0.47870305,
                    0.45479696,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            ]
        )
        print(blurred_frame)
        assert np.allclose(blurred_frame, expected_frame)
