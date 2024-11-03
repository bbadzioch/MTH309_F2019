import matplotlib.pyplot as plt
import numpy as np
from sympy import *

init_printing(use_latex='mathjax')

def paste_image(background, foreground, coord_change):
    '''
    Pastes an image into a quadrilateral area of the background image defined by four vertices.

    background:  
        The name of the background image file
    foreground:  
        The name of the foreground image file
    coord_change:
        The 3x3 change of coordinates matrix from the background image coordinates
                 to the camera coordinates


    Returns a 3-dimensional numpy array representing modified background image
    '''

    img = plt.imread(foreground)
    if (len(img.shape) == 3) and (img.shape[2] > 3):
        img = img[:, :, :3]
    background = plt.imread(background)
    if (len(background.shape) == 3) and (background.shape[2] > 3):
        background = background[:, :, :3]


    if img.dtype == 'uint8':
        img = img.astype(float)/255

    if background.dtype == 'uint8':
        background = background.astype(float)/255


    brows, bcols = background.shape[:2]
    irows, icols = img.shape[:2]

    A = np.array(coord_change).astype(float)
    B = np.array([[1, 0, 0], [0, icols-1, 0], [0, 0, irows-1]]).T
    CB = np.dot(B, np.linalg.inv(A))


    #for each pixel of the background image compute coordinates of
    #the corresponding pixel in the pasted image
    indices = np.empty((brows, bcols, 3))
    indices[:,:,1], indices[:,:,2] = np.meshgrid(np.arange(bcols), np.arange(brows))
    indices[:,:,0] = 1
    background_coords = indices.reshape(-1, 3).T
    img_coords = np.dot(CB, background_coords)
    homog_coords = (img_coords/img_coords[0]).astype(int)

    # some of these coordinates in the pasted image computed above may be
    # negative or exceed pasted image dimensions; they correspond to background image
    # pixels that lay outside the area defined by vertices
    # below we select coordinates that are valid
    valid_homog_bool  = (0 <= homog_coords[1]) & (0 <= homog_coords[2]) & (homog_coords[1] < icols) & (homog_coords[2] < irows)
    valid_homog_coords = homog_coords[:, valid_homog_bool]

    #copy pixels from the pasted image to the background image
    img_indices = np.ravel_multi_index([valid_homog_coords[2], valid_homog_coords[1]], img.shape[:2])
    background_array = background.copy().reshape(-1, 3).T
    background_array[:, valid_homog_bool] =  img.reshape(-1, 3).T[:, img_indices]

    return background_array.T.reshape(brows, bcols, 3)
