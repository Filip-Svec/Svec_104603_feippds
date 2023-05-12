"""This module implements image converting function to greyscale.

This implementation uses numba library to parallelize computation
of conversion of an image to greyscale.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Filip Švec, Tomáš Vavro, Marián Šebeňa"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk, mariansebena@stuba.sk"
__license__ = "MIT"

import os
from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import time


def grayscale_CPU(image):
    """Convert an RGB image to grayscale with CPU.

    Args:
        image - image data

    Returns:
        A 2D NumPy array of shape (height, width) representing the grayscale image.
    """
    return image[:, :, 0] * 0.21 + image[:, :, 1] * 0.72 + image[:, :, 2] * 0.07


@cuda.jit
def grayscale_kernel(image, gray):
    """A CUDA kernel that converts a 3-channel RGB image to grayscale.

        Args:
            image: the input image.
            gray: the output grayscale image.
    """

    row, col = cuda.grid(2)  # Get the thread's row and column indices
    if row < image.shape[0] and col < image.shape[1]:
        r, g, b = image[row, col]
        gray[row, col] = 0.21 * r + 0.72 * g + 0.07 * b


def grayscale(image):
    """Convert an image to grayscale using CUDA.

        Args:
            image - image data

        Returns:
            output_image
    """

    # Get the dimensions of the input image
    height, width, channels = image.shape
    print(f'width: {width}, height: {height}')

    # Allocate memory for the input and output images on the GPU
    d_input_image = cuda.to_device(image)
    d_output_image = cuda.device_array((height, width), dtype=np.float32)

    # Set the number of threads per block and the number of blocks per grid
    threads_per_block = (16, 16)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Launch the kernel to convert the image to grayscale
    grayscale_kernel[blocks_per_grid, threads_per_block](d_input_image, d_output_image)

    # Copy the grayscale image back to the CPU
    output_image = d_output_image.copy_to_host()

    return output_image


def main():
    """Run main."""
    directory = "imgz/"
    files = os.listdir(directory)

    # Loop through all files using GPU
    for filename in files:
        print(filename)
        start_time = time.time()
        image = plt.imread("imgz/" + filename)
        newImage = grayscale(image)
        print("--- %s seconds ---" % (time.time() - start_time))
        plt.imsave("imgz_grey/" + "grey_" + filename, newImage, cmap='gray', format="jpg")

    # Loop through all files using CPU
    for filename in files:
        print(filename)
        start_time = time.time()
        image = plt.imread("imgz/" + filename)
        grayscale_CPU(image)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
