import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float,measure
from scipy import ndimage as ndi
import czifile

#circularity filter
#or (4*np.pi*region.area)/region.perimeter^2 < drop_circ
#drop_circ=0.5,




def load_img(file, crop=None, display=False): #defines function for image loading, takes file as argument as well as crop (to remove scale bar) and display option
    if file.suffix == ".czi":
        img = czifile.imread(file).squeeze() #!!
        return img
        if len(img.shape) == 3:
            img = img[img.sum(axis=(1,2)).argmax()] #!!
    else:
        img = np.mean(img_as_float(io.imread(file)), axis=2) #reads in .tifs

    if crop is not None:
        img = img[:crop] #crops image if crop argument is given
    if display:
        plt.imshow(img, interpolation='none')
        plt.show() #displays image for manual check 
    return img


def get_droplet_mask(img, n_std, min_area=0, max_area=np.inf, display=False):
    im_mean = np.mean(img)
    im_std = np.std(img)
    std_from_mean = (img - im_mean) / im_std
    droplet_scaffold_mask = std_from_mean > n_std
    droplet_mask = ndi.morphology.binary_fill_holes(droplet_scaffold_mask)
    droplet_mask_labeled = measure.label(droplet_mask)
    droplet_region_props = measure.regionprops(droplet_mask_labeled)
    for region in droplet_region_props:
        if region.area < min_area or region.area > max_area:
            droplet_mask[region.coords[:, 0], region.coords[:, 1]] = 0

    droplet_mask_labeled = measure.label(droplet_mask)
    droplet_region_props = measure.regionprops(droplet_mask_labeled, img)
    if display:
        plt.imshow(droplet_mask, interpolation='none')
        plt.show()
    return droplet_mask, droplet_region_props
