import pytest
import numpy as np
import sys
from logic.utils.imageProcessing import gaussian_kernel, convolve


class TestImageProcessingFunctions:

    def test_gaussian_kernel_default_sigma(self) -> None:
        # Test case 1: Test Gaussian kernel with default sigma
        size = 3
        kernel = gaussian_kernel(size)
        assert np.allclose(
            kernel,
            np.array(
                [
                    [0.07511361, 0.1238414, 0.07511361],
                    [0.1238414, 0.20417996, 0.1238414],
                    [0.07511361, 0.1238414, 0.07511361],
                ]
            ),
        )

    def test_gaussian_kernel_custom_sigma(self) -> None:
        # Test case 2: Test Gaussian kernel with custom sigma
        sigma = 0.5
        size = 3
        kernel = gaussian_kernel(size, sigma)
        assert np.allclose(
            kernel,
            np.array(
                [
                    [0.01134374, 0.08381951, 0.01134374],
                    [0.08381951, 0.61934703, 0.08381951],
                    [0.01134374, 0.08381951, 0.01134374],
                ]
            ),
        )
