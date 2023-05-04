from numba import cuda
import matplotlib.pyplot as plt
import numpy as np
# import math
import time

# Grayscale formula: https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html
@cuda.jit
def grayscale_kernel(input_image, output_image):
    x, y = cuda.grid(2)
    if x < output_image.shape[0] and y < output_image.shape[1]:
        r, g, b = input_image[x, y]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        output_image[x, y] = (gray, gray, gray)

def grayscale_host(input_image):
    height, width, channels = input_image.shape
    output_image = np.zeros((height, width, channels), dtype=np.uint8)

    for row in range(height):
        for col in range(width):
            # Get the RGB values of the current pixel
            r, g, b = input_image[row, col]

            # Apply the grayscale formula to compute the gray value
            gray_value = 0.299 * r + 0.587 * g + 0.114 * b

            # Set the corresponding pixel in the output image to the gray value
            output_image[row, col] = (gray_value, gray_value, gray_value)
    return output_image

def main_host():
    filename = input("Filename: ")

    pixels = plt.imread(filename)

    start_time = time.time()

    output_pixels = grayscale_host(pixels)

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")

    plt.imsave(filename.split(".")[0] + "_grey.jpg", output_pixels, format="jpg")

def main_kernel():
    filename = input("Filename: ")

    pixels = plt.imread(filename)

    start_time = time.time()

    device = cuda.get_current_device()
    tpb = (device.WARP_SIZE, device.WARP_SIZE)
    image_shape = pixels.shape[:2]
    # bpg = tuple(np.ceil(np.array(image_shape) / tpb).astype(int))
    bpg = (np.ceil(image_shape[0] / tpb[0]).astype(int), np.ceil(image_shape[1] / tpb[1]).astype(int))

    input_image_device = cuda.to_device(pixels)
    output_image_device = cuda.device_array(image_shape + (3,), dtype=np.uint8)

    grayscale_kernel[bpg, tpb](input_image_device, output_image_device)

    output_pixels = output_image_device.copy_to_host()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")

    plt.imsave(filename.split(".")[0]+"_grey.jpg", output_pixels, format="jpg")

if __name__ == '__main__':
    # main_kernel()
    main_host()