import numpy as np
import pywt
import matplotlib.pyplot as plt
from osgeo import gdal
from PIL import Image
import matplotlib.image
from tkinter import messagebox
import cv2
from skimage.restoration import (estimate_sigma)
import os.path

def lee_filter(im, kernel = 3):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []

    pad = int((kernel-1)/2)
    extended = np.array(pywt.pad(im, pad, 'symmetric'))

    h,w = np.shape(extended)
    sigma = np.var(im)

    denoised = np.zeros(np.shape(im))

    for i in range(pad, h-pad):
        for j in range(pad, w-pad):
            window = extended[i-pad:i+pad+1, j-pad:j+pad+1]

            window_mean = np.nanmean(window)
            window_sigma = np.nanvar(window)
            weighted_function = window_sigma/(sigma+(window_sigma))

            new_value = window_mean + (weighted_function*(np.take(window, window.size//2)-window_mean))

            denoised[i-pad, j-pad] = new_value

    return denoised 

def kuan_filter(im, kernel = 3):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []

    pad = int((kernel-1)/2)
    extended = np.array(pywt.pad(im, pad, 'symmetric'))

    h,w = np.shape(extended)
    sigma = np.var(im)

    denoised = np.zeros(np.shape(im))

    for i in range(pad, h-pad):
        for j in range(pad, w-pad):
            window = extended[i-pad:i+pad+1, j-pad:j+pad+1]

            window_mean = np.nanmean(window)
            window_sigma = np.nanvar(window)
            weighted_function = (1-(window_sigma/sigma))/(1+window_sigma)

            new_value = window_mean + (weighted_function*(np.take(window, window.size//2)-window_mean))

            denoised[i-pad, j-pad] = new_value

    return denoised 

def local_weight_matrix(window, factor_a):    
    flat = window.flatten()
    center = np.take(window, window.size//2)

    distances =  np.abs(flat - center)

    weights = np.exp(-factor_a ** distances)

    return weights


def frost_filter(im, kernel = 3, damp_factor = 1):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []

    pad = int((kernel-1)/2)
    extended = np.array(pywt.pad(im, pad, 'symmetric'))

    h,w = np.shape(extended)
    sigma = np.var(im)

    denoised = np.zeros(np.shape(im))

    for i in range(pad, h-pad):
        for j in range(pad, w-pad):
            window = extended[i-pad:i+pad+1, j-pad:j+pad+1]

            window_mean = np.nanmean(window)
            window_sigma = np.nanvar(window)
            
            sigma_zero = window_sigma /(window_mean**2)
            factor_A = damp_factor * sigma_zero

            weights = local_weight_matrix(window, factor_A)
            values = window.flatten()

            weighted_values = weights * values

            denoised[i-pad, j-pad] = weighted_values.sum()/weights.sum()

    return denoised

def median_filter(img, kernel):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []
    try:
        denoised = cv2.medianBlur((img), kernel)
    except:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        denoised = cv2.medianBlur(cv2.convertScaleAbs(img), kernel)
    

    return denoised

def mean_filter(img, kernel):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []

    denoised = cv2.blur(img, (kernel, kernel))

    return denoised

def gaussian_filter(img, kernel, sigma = 2):
    if kernel % 2 == 0:
        messagebox.showerror("ERROR", "Kernel MUST be an ODD number.")
        return []

    denoised = cv2.GaussianBlur(img, (kernel, kernel), sigma)

    return denoised

def wavelet_filter(img, J = 2, w = "db2", thresh = "soft"):
    coeffs = pywt.wavedecn(img, w, level = J)
    array, slices = pywt.coeffs_to_array(coeffs)

    sigma = estimate_sigma(img, average_sigmas=True)
    n = np.shape(img)[0]**2
    t = sigma*np.sqrt(2*np.log(n))

    thresholded = pywt.threshold(array, t, mode=thresh)

    coeffs = pywt.array_to_coeffs(thresholded, slices)
    denoised = pywt.waverecn(coeffs, w)

    return denoised

def verify_directory(input, output):
    inp = os.path.isfile(input)
    out = os.path.isdir(output)

    if (inp == True) and (out == False):
        messagebox.showerror("ERROR", "Output file directory is invalid.")
        return False
    if (inp == False) and (out == True):
        messagebox.showerror("ERROR", "Input file directory is invalid.")
        return False
    if (inp == False) and (out == False):
        messagebox.showerror("ERROR", "Both input and output file directories are invalid.")
        return False

    return True

def run_wavelet(filetype, wvt, thresh, J, input, output):
    if verify_directory(input, output) == False:
        return

    img = []

    if filetype == 'png':
        img = np.asarray(Image.open(input).convert("L"))
    elif filetype == 'tif':
        img_tiff = gdal.Open(input)
        img_array = img_tiff.ReadAsArray().astype(float)
        img = np.nansum(np.square(np.dstack((img_array))), axis = 2)

    denoised = wavelet_filter(img, J, wvt, thresh)

    matplotlib.image.imsave(f'{output}/Wavelet_{wvt}_img.png', np.asarray(denoised), cmap = 'gray')
    fig = plt.figure()

    fig.add_subplot(1,2,1)
    plt.imshow(img, cmap = "gray")
    plt.title("Original Image")
    plt.axis('off')

    fig.add_subplot(1,2,2)
    plt.imshow(denoised, cmap = "gray")
    plt.title("Wavelet Filtered Image")
    plt.axis('off')

    plt.show()

    messagebox.showinfo("Message", f"The filtered image has been saved in the output directory {output} with the name Wavelet_{wvt}_img.png. Make sure to change the file name because it can be replaced in the next execution of the filter for this output directory. ")


def run_filter(filter, kernel, filetype, input, output, damp_factor = 1, sigma = 2):
    if verify_directory(input, output) == False:
        return
    
    img = []
    denoised = []
    if filetype == 'png':
        img = np.asarray(Image.open(input).convert("L"))
    elif filetype == 'tif':
        img_tiff = gdal.Open(input)
        img_array = img_tiff.ReadAsArray().astype(float)
        img = np.nansum(np.square(np.dstack((img_array))), axis = 2)

    if filter == "Lee":
        denoised = lee_filter(img, kernel)
    if filter == "Kuan":
        denoised = kuan_filter(img, kernel)
    if filter == "Frost":
        denoised = frost_filter(img, kernel, damp_factor)
    if filter == "Gaussian":
        denoised = gaussian_filter(img, kernel, sigma)
    if filter == "Mean":
        denoised = mean_filter(img, kernel)
    if filter == "Median":
        denoised = median_filter(img, kernel)

    if denoised == []:
        return

    matplotlib.image.imsave(f'{output}/{filter}_img.png', np.asarray(denoised), cmap = 'gray')
    fig = plt.figure()

    fig.add_subplot(1,2,1)
    plt.imshow(img, cmap = "gray")
    plt.title("Original Image")
    plt.axis('off')

    fig.add_subplot(1,2,2)
    plt.imshow(denoised, cmap = "gray")
    plt.title(f"{filter} Filtered Image")
    plt.axis('off')

    plt.show()

    messagebox.showinfo("Message", f"The filtered image has been saved in the output directory {output} with the name {filter}_img.png. Make sure to change the file name because it can be replaced in the next execution of the filter for this output directory. ")



