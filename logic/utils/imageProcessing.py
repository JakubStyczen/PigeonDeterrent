import numpy as np


def gaussian_kernel(size, sigma: float = 1.0) -> np.array:
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    kernel_exp_part = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
    # coefficent = 1 / (2.0 * np.pi * sigma**2.0)
    kernel_exp_part /= np.sum(kernel_exp_part)
    return kernel_exp_part


def convolve(image: np.array, kernel: np.array) -> np.array:
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image.shape
    half_kenrel_height, half_kenrel_width = kernel_height // 2, kernel_width // 2

    convolved_image = np.zeros((image_height, image_width))

    for i in range(image_height - kernel_height + 1):
        for j in range(image_width - kernel_width + 1):

            context = image[i : i + kernel_width, j : j + kernel_height]

            convolved_image[i + half_kenrel_width, j + half_kenrel_height] = np.sum(
                context * kernel
            )

    return convolved_image
