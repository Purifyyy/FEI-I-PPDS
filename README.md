# Assignment 05

[![Python 3.10.4](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/release/python-3104/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-red.svg)](https://conventionalcommits.org)

## Assignment introduction

Pixel processing that utilizes computing power of CPU can be tedious and lengthy task. Especially when performing operations (like grayscaling), with pixels of higher resolution images. Fortunately, utilizing GPU with NVIDIAs parallel computing platform CUDA, this process, can be done more efficiently.

## CPU vs GPU

The process of image grayscaling on a GPU, can be performed more effectively because it utilizes a special approach of executing instructions, called **SIMD**. Single Instruction Multiple Data or SIMD, takes advantage of the situation where we multiply large number of data points with the same value. [[1]](#1) On the other hand **SISD**, an approach utilized by CPU, is a traditional, sequential type of instruction execution in which a single instruction operates on a single piece of data. [[2]](#1)

## Terminologies in CUDA

In CUDA applications a **host** function is understood as a function that is called from CPU and can only be executed on it. Likewise a **device** function is called from GPU and can only be executed on it. A **kernel** (global) denotes a function that is called from the CPU, but is executed on the GPU. For computation, CUDA uses **threads**. Threads form a 3-dimensional organisational structure. Threads form blocks, and blocks form grids. All threads in a grid perform the same kernel function, and each thread has a unique identifier.

## Overview of important implementation parts

Our application defines several functions, most importantly a `grayscale_kernel(input_image, output_image)`, that is called from CPU but is being perfomed on GPU. Since kernel function cannot return data, in adition to the `input_image` we must also provide a `output_image` variable for the data to be transported back. With `cuda.grid(2)` call, we get the **x** and **y** coordinates of the current thread in the entire grid of blocks. This is used to determine which pixel of the input and output images the current thread should operate on. After that, a check if current thread is not processing pixels outside the bounds of the image is perfomed. Finally RGB values are extracted from the input image, and assigned to the output image after a grayscale conversion was performed on them using a [conversion formula](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html).

A `grayscale_host(input_image)` function, performing grayscaling on CPU is also defined. This function simply defines a output image variable, based on size of the input image, and using the same formula as mentioned above, computes each pixel via nested for loop. When all pixels are processed, the function returns the output image.

For completeness `main_host()` manages the operation of image loading and saving when performing CPU grayscaling. Similarly `main_kernel()` manages the same operations when using GPU, but additionally sets the amount of threads per block, and blocks per grid.

## Performance comparison

Displayed in the table is time of grayscale conversion of image using GPU and CPU. The average is based on 5 independent runs. This experiment was carried out with Ryzen 5 1600 (stock clock speed) and GeForce GTX 1060 6GB (clocked @1825MHz).

| Image        | Size [px] | Average GPU time [s] | Average CPU time [s] |
| ------------ | --------- | -------------------- | -------------------- |
| fruit.jpg    | 128x73    | 0.48434176445007 *   | 0.085507583618164    |
| mortar.jpg   | 300x200   | 0.49175519943237 *   | 0.55863475799561     |
| deer.jpg     | 480x600   | 0.51212697029114     | 2.6973008155823      |
| flowers.jpg  | 960x596   | 0.49886431694031     | 5.2561017990112      |
| r8.jpg       | 1600x941  | 0.49440631866455     | 14.240615606308      |
| pumpkin.jpg  | 2560x1707 | 0.50730056762695     | 42.075201320648      |
| graffiti.jpg | 6000x4000 | 0.56236615180969     | 226.2164766472       |

\* - GPU under-utilization due to low occupancy of the grid

From the displayed data, we may conclude that computing grayscale conversion of an image on GPU using CUDA, is much more efficient, from as small a resolution as 480x600. Computing tiny images (300x200 or smaller) using CUDA resulted in GPU under-utilization, so the average time was comparable to computation using CPU.

### Conversion sample preview

Following images show pre and post grayscale conversion of mentioned fruit.jpg, graffiti.jpg and r8.jpg images respectively. (for showcase purposes, all of the images were scaled to the same height)

![](https://i.imgur.com/65YnMnj.jpeg)

![](https://i.imgur.com/WdSDjhb.jpeg)

![](https://i.imgur.com/pMeWBV3.jpeg)

Disclaimer: I do not claim ownership of images used in this showcase, they are property of their respective owners.

## Installation guide

In order to run our grayscale conversion script, a [NumPy]([NumPy - Installing NumPy](https://numpy.org/install/)), [Numba]([Installation &mdash; Numba 0.57.0+0.g4fd4e39c6.dirty documentation](https://numba.readthedocs.io/en/stable/user/installing.html)), [matplotlib]([Installation &#8212; Matplotlib 3.7.1 documentation](https://matplotlib.org/stable/users/installing/index.html)) python packages are required. Python version 3.8–3.10 is also required. Numba is compatible with NumPy versions 1.21–1.24. Additionally a CUDA capable GPU is necessary, along with the [CUDA toolkit]([CUDA Toolkit Archive | NVIDIA Developer](https://developer.nvidia.com/cuda-toolkit-archive)). 

## References

<a id="1">[1]</a> 
SIMD architectures | Ars Technica 
https://arstechnica.com/features/2000/03/simd/

<a id="1">[2]</a> 
MICHAEL J. FLYNN.
Some Computer Organizations and Their Effectiveness