import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

init_printing(use_latex='mathjax')

def color_mixer(A, img, width=8, height=12):
    
    A = np.array(A).astype(float)
    
    if img.dtype == 'uint8':
        img = img.astype(float)/255
    
    new_img = np.transpose(np.dot(A, np.transpose(img, axes = (0, 2, 1))), axes = (1, 2, 0))
    new_img[new_img < 0] = 0
    new_img[new_img > 1] = 1
    new_img = (255*new_img).astype('uint8')
    plt.figure(figsize=(width,height))
    plt.imshow(new_img)
    plt.show()


def color_sample(*rgb):
    if np.min(rgb) < 0 or np.max(rgb) > 255:
        print("ERROR: RGB coordinates must be intergers in the range 0-255.")
        return None
    rgb = np.array(rgb).astype('uint8')
    sample = np.ones((10,10, 3), dtype='uint8')*rgb
    plt.figure(figsize = (2.5,2.5))
    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("R {}    G {}    B {}".format(rgb[0], rgb[1], rgb[2]))
    ax.imshow(sample)
    plt.show()