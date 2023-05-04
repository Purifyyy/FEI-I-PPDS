from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import time

# Grayscale formula: https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html
@cuda.jit
def grayscale_kernel(input_image, output_image):
    x, y = cuda.grid(2)
    if x < output_image.shape[0] and y < output_image.shape[1]:
        r, g, b = input_image[x, y]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        output_image[x, y] = (gray, gray, gray)

def main():
    filename = input("Filename: ")

    pixels = plt.imread(filename)

    # start_time = time.time()

    device = cuda.get_current_device()
    tpb = (device.WARP_SIZE, device.WARP_SIZE)
    image_shape = pixels.shape[:2]
    bpg = tuple(np.ceil(np.array(image_shape) / tpb).astype(int))

    input_image_device = cuda.to_device(pixels)
    output_image_device = cuda.device_array(image_shape + (3,), dtype=np.uint8)

    grayscale_kernel[bpg, tpb](input_image_device, output_image_device)

    output_pixels = output_image_device.copy_to_host()

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time:.2f} seconds")

    plt.imsave(filename.split(".")[0]+"_grey.jpg", output_pixels, format="jpg")

if __name__ == '__main__':
    main()