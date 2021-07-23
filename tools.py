import numpy as np
from load import get_droplet_mask
import matplotlib.pyplot as plt


def subtract_off_mean_background_intensity(img, nstd=0, min_area=0, max_area=np.inf, display=False):
    mask, props = get_droplet_mask(img, n_std=nstd, min_area=min_area, max_area=max_area)
    mean_background =  img[~mask].mean()
    if display:
        plt.subplot(121)
        plt.imshow(img)
        plt.subplot(122)
        plt.imshow(~mask)
        plt.show()
    return img - mean_background


def line_hist(data, label=None, **kwargs):
    hist, bin_edges = np.histogram(data, **kwargs)
    xaxis = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.plot(xaxis, hist, marker="o", label=label)