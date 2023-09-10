import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
import skimage
import pywt
import matplotlib.colors
import matplotlib.image
from PIL import Image
import cv2 
import matplotlib.patches
import os
from tkinter import messagebox
import numba



def scale(im):
    scaled = (im - np.nanmin(im))/(np.nanmax(im)-np.nanmin(im))
    return im

def find_crop(h,w):
    sh = 1
    sw = 1

    while(h%4!=0):
        h = h+sh
        sh = sh+1

    while(w%4!=0):
        w = w+sw
        sw = sw+1

    return (h,w)

def extend_images(images):
    h,w = np.shape(images[0])
    n = len(images)

    power = np.ceil(np.log2(np.min([h, w])))
    two_powered = (2 ** power).astype(int)

    padding = np.ceil((two_powered - np.min([h, w]))/2).astype(int)
    crop_h, crop_w = find_crop(padding+h, padding+w)

    extended = []
    for i in range(0, n):
        norm = np.linalg.norm(images[i])
        new_im = pywt.pad(images[i]/norm, padding, 'periodization')
        cropped = new_im[0:crop_h,0:crop_w]

        extended.append(cropped)
    
    return (np.array(extended), padding)

def calculate_wavelet_images(images):
    #image dimension has to be mutiple of 2^J (in this case J = 2)
    extended, padding = extend_images(images) 
    h,w = np.shape(images[0])
    n = len(extended)

    x = []
    for i in range(0, n):
        wavelet = pywt.swtn(extended[i], wavelet="db2", level=2, trim_approx=True)
        approx_coeffs = np.array(wavelet[0])[padding:padding+h, padding:padding+w]

        x.append(approx_coeffs)

    return np.array(x)

@numba.jit(nopython=True, parallel=True, cache=True)
def calculate_dmatrices(x_images, mean_image):
    n = len(x_images)
    d_matrices = np.empty((n, *x_images[0].shape))

    for i in numba.prange(n):
        d_matrices[i] = np.square(x_images[i] - mean_image)

    return d_matrices

@numba.jit(nopython=True, parallel=True, cache=True)
def calculate_R(tensor, vector):
    h, w, d = tensor.shape
    corr = np.zeros((h, w))

    vector_mean = 0
    vector_std = 0

    for k in range(d):
        vector_mean += vector[k]
        vector_std += vector[k] * vector[k]

    vector_mean /= d
    vector_std = vector_std / d - vector_mean * vector_mean
    vector_std = vector_std**0.5

    for i in numba.prange(h):
        for j in numba.prange(w):
            mean = 0
            std = 0

            for k in range(d):
                mean += tensor[i, j, k]
                std += tensor[i, j, k] * tensor[i, j, k]

            mean /= d
            std = std / d - mean * mean
            std = std**0.5

            corr_ij = 0
            for k in range(d):
                corr_ij += (tensor[i, j, k] - mean) * (vector[k] - vector_mean)

            corr_ij /= d
            corr_ij /= std * vector_std

            corr[i, j] = abs(corr_ij)

    return corr

def show_images(images):
    p = plt.figure()

    p.add_subplot(1,2,1)
    plt.imshow(images[0], cmap = 'gray')
    plt.title('First image')
    plt.axis('off')

    p.add_subplot(1,2,2)
    plt.imshow(images[len(images)-1], cmap = 'gray')
    plt.title('Last image')
    plt.axis('off')

    plt.annotate('While this window is open, the method is frozen. \nClose to continue execution.',
            xy = (1.0, -0.2),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)
    plt.show() 

def change_map_otsu(R):
    R_grayscale = np.array(Image.fromarray(np.uint8(R * 255) , 'L'))
    o = skimage.filters.threshold_otsu(R_grayscale)
    binary_mask = R_grayscale > o

    return binary_mask

def read_time_series(input):
    images = []

    #Reading images
    for file in os.listdir(input):
        im = gdal.Open(os.path.join(input, file))
        imarray = im.ReadAsArray().astype(float)
        im_comb = (np.nansum(np.square(np.dstack(scale(imarray))), axis = 2))
        print(f'{file}: {np.shape(im_comb)}')
        images.append(im_comb)
    
    images = np.asarray(images)
    return images

def change_map_kmeans(R, k):
    flat = np.float32(R.flatten())
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0002)

    _, labels, (centers) = cv2.kmeans(flat, k, None, criteria, 10,  cv2.KMEANS_RANDOM_CENTERS)

    labels = labels.flatten()
    res = centers[labels]
    change = np.nanmax(centers) #high correlation values represent change
    binary_mask = np.where((res == change), 1, 0).reshape(np.shape(R))

    return binary_mask

def show_results(R, otsu, k3, k4):
    cmap = matplotlib.colors.ListedColormap(['lightgreen', 'red'])
    fig = plt.figure()

    fig.add_subplot(2,2,1)
    plt.imshow(R, cmap='rainbow')
    plt.colorbar()
    plt.title("Correlation Matrix")
    plt.axis('off')

    fig.add_subplot(2,2,2)
    plt.imshow(otsu, cmap=cmap)
    plt.title("Otsu thresholding")
    plt.axis('off')

    fig.add_subplot(2,2,3)
    plt.imshow(k3, cmap=cmap)
    plt.title("Kmeans with K=3")
    plt.axis('off')

    fig.add_subplot(2,2,4)
    plt.imshow(k4, cmap=cmap)
    plt.title("Kmeans with K=4")
    plt.axis('off')

    plt.show()

def verify_directory(input, output):
    inp = os.path.isdir(input)
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

def run_wecs(input, output):
    if verify_directory(input, output) == False:
        return

    images = read_time_series(input)
    if len(np.shape(images))!=3:
        messagebox.showerror("Images MUST have same dimensions.")
        return

    show_images(images)

    #Reference image
    mean_image = sum(images)/len(images)
    norm = np.linalg.norm(mean_image)
    mean_image = mean_image/norm

    #Wavelet images
    print('mean image calculated')
    x_images = calculate_wavelet_images(images)

    #Squared deviations matrices
    print('x images calculated')
    d_matrices = calculate_dmatrices(x_images, mean_image)

    #Overall change
    d_vector = np.sum(d_matrices, axis=(1, 2))

    #Correlation matrix
    print('R calculating')
    R = calculate_R(d_matrices.T, d_vector).T

    #Binary maps
    cm_otsu = change_map_otsu(R)
    cm_kmeans_3 = change_map_kmeans(R, 3)
    cm_kmeans_4 = change_map_kmeans(R, 4)

    print('thresholding done')
    show_results(R, cm_otsu, cm_kmeans_3, cm_kmeans_4)

    cmap = matplotlib.colors.ListedColormap(['lightgreen', 'red'])
    matplotlib.image.imsave(f'{output}/change_map_otsu.png', np.asarray(cm_otsu), cmap=cmap)
    matplotlib.image.imsave(f'{output}/change_map_kmeans_3.png', np.asarray(cm_kmeans_3), cmap=cmap)
    matplotlib.image.imsave(f'{output}/change_map_kmeans_4.png', np.asarray(cm_kmeans_4), cmap=cmap)
    matplotlib.image.imsave(f'{output}/correlation_matrix_R.png', np.asarray(R), cmap='rainbow')

    messagebox.showinfo("MESSAGE", f"The change maps and correlation matrix have been saved in the folder {output}. Make sure to rename all files because they may be replaced in the next execution of the method with the same output.")
