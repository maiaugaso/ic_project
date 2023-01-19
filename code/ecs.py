import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
from  matplotlib.colors import LinearSegmentedColormap
import skimage
import pywt
import matplotlib.colors
import matplotlib.image
from PIL import Image
import glob 
import cv2 
import matplotlib.patches
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.cluster import KMeans
import os
from tkinter import messagebox


def scale(im):
    scaled = (im - np.nanmin(im))/(np.nanmax(im))
    return scaled

def calculate_dmatrices(images, mean_image):
    n = len(images)
    d_matrices = []

    for i in range(0, n):
        norm = np.linalg.norm(images[i])
        d_i = np.square(images[i]/norm - mean_image)
        d_matrices.append(d_i)

    return np.array(d_matrices)

def calculate_R(d_matrices, d_vector):
    h,w = np.shape(d_matrices[0])
    R = np.zeros((h,w))

    for i in range(0, h):
        for j in range(0, w):
            dij = d_matrices[:,i,j]
            rij = np.corrcoef(dij, d_vector)[0,1]
            R[i,j] = abs(rij)

    return R

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
    grayscale = np.array(Image.fromarray(np.uint8(R * 255) , 'L'))
    o = skimage.filters.threshold_otsu(grayscale)
    binary_mask = grayscale > o

    return binary_mask

def read_time_series():
    images = []

    #Reading images
    directory = 'code/IMAGE_SERIES/'
    for file in os.listdir(directory):
        im = gdal.Open(os.path.join(directory, file))
        imarray = im.ReadAsArray().astype(float)
        im_comb = (np.nansum(np.square(np.dstack(scale(imarray))), axis = 2))
        images.append(im_comb)
    
    return images

def change_map_kmeans(R, k):
    flat = np.float32((np.nan_to_num(R)).flatten())
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

def run_ecs():
    images = read_time_series()
    if len(np.shape(images))!=3:
        messagebox.showinfo("Images MUST have same dimensions.")
        return

    show_images(images)

    #Reference image
    mean_image = sum(images)/len(images)
    norm = np.linalg.norm(mean_image)
    mean_image = mean_image/norm

    #Squared deviations matrices
    d_matrices = calculate_dmatrices(images, mean_image)

    #Overall change
    d_vector = np.array(list(map(np.sum, d_matrices)))

    #Correlation matrix
    R = calculate_R(d_matrices, d_vector)
    plt.hist(R)
    plt.show()

    #Binary maps
    cm_otsu = change_map_otsu(R)
    cm_kmeans_3 = change_map_kmeans(R, 3)
    cm_kmeans_4 = change_map_kmeans(R, 4)

    show_results(R, cm_otsu, cm_kmeans_3, cm_kmeans_4)

    cmap = matplotlib.colors.ListedColormap(['lightgreen', 'red'])
    matplotlib.image.imsave('code/CHANGE_MAPS/ECS/change_map_otsu.png', np.asarray(cm_otsu), cmap = cmap)
    matplotlib.image.imsave('code/CHANGE_MAPS/ECS/change_map_kmeans_3.png', np.asarray(cm_kmeans_3), cmap = cmap)
    matplotlib.image.imsave('code/CHANGE_MAPS/ECS/change_map_kmeans_4.png', np.asarray(cm_kmeans_4), cmap = cmap)
    matplotlib.image.imsave('code/CHANGE_MAPS/ECS/correlation_matrix_R.png', np.asarray(R), cmap = 'rainbow')

    messagebox.showinfo("MESSAGE", "The change maps and correlation matrix have been saved in the folder \'code/CHANGE_MAPS/ECS\'. Make sure to transport it to your own storage because the files will be lost in the next execution of the method.")

