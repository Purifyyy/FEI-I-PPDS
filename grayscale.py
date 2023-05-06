"""
Image grayscaling module.

This module provides functions to process image and perform grayscale on it.
Grayscale can be performed both using the computational power of CPU or GPU.
"""


__authors__ = "Tomáš Baďura"


from numba import cuda
import matplotlib.pyplot as plt
import numpy as np
import time


@cuda.jit
def grayscale_kernel(input_image, output_image):
    """
    Performs grayscale on input_image and saves the result into output_image.
    Grayscale is computed using CUDA threads.

    Arguments:
        input_image (DeviceNDArray) -- Numba's representation of NumPy array, containing the pixels of inputted image
        output_image (DeviceNDArray) -- Numba's representation of empty NumPy array, with identical shape as input_image
    """
    x, y = cuda.grid(2)
    if x < output_image.shape[0] and y < output_image.shape[1]:
        r, g, b = input_image[x, y]
        # Grayscale formula: https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        output_image[x, y] = (gray, gray, gray)


def grayscale_host(input_image):
    """
    Performs grayscale on input_image and returns the result as output_image.

    Arguments:
        input_image (numpy.array) -- the inputted image pixel data of shape (height, width, 3)

    Returns:
        output_image (numpy.array) -- the grayscale computed from input_image
    """
    height, width, channels = input_image.shape
    output_image = np.zeros((height, width, channels), dtype=np.uint8)
    for row in range(height):
        for col in range(width):
            r, g, b = input_image[row, col]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            output_image[row, col] = (gray, gray, gray)
    return output_image


def main_host():
    """
    Image processing function for grayscale_host().
    Reads image as filename, performs grayscale using grayscale_host() function and saves it.
    Function also measures time of grayscale computation.
    """
    filename = input("Filename: ")
    input_image = plt.imread(filename)

    start_time = time.time()

    output_image = grayscale_host(input_image)

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")

    plt.imsave(filename.split(".")[0] + "_gray.jpg", output_image, format="jpg")


def main_kernel():
    """
    Image processing function for grayscale_kernel().
    Reads image as filename, sets thread and block amount in CUDA grid, processes inputted image and prepares output
    to appropriate representation. Performs grayscale using grayscale_kernel() function and saves it.
    Function also measures time of grayscale computation.
    """
    filename = input("Filename: ")
    pixels = plt.imread(filename)

    start_time = time.time()

    device = cuda.get_current_device()
    tpb = (device.WARP_SIZE, device.WARP_SIZE)

    image_shape = pixels.shape[:2]
    # calculates the number of blocks needed to cover an image of a given shape
    bpg = (np.ceil(image_shape[0] / tpb[0]).astype(int), np.ceil(image_shape[1] / tpb[1]).astype(int))

    input_image = cuda.to_device(pixels)
    # creates empty device array in GPU memory, that has the same shape as the input image
    output_image = cuda.device_array(image_shape + (3,), dtype=np.uint8)

    grayscale_kernel[bpg, tpb](input_image, output_image)

    output_pixels = output_image.copy_to_host()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")

    plt.imsave(filename.split(".")[0]+"_gray.jpg", output_pixels, format="jpg")


if __name__ == '__main__':
    # main_host()
    main_kernel()
