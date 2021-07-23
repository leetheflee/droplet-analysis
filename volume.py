from czifile import imread
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np

img = imread("/mnt/c/Users/Leo/Google Drive/..Uni/Masters/Droplet analysis/droplet_analysis_Wilkinson/confocal data/mCherry-1_z-stack.czi")
img = np.squeeze(img)
img_mean = img.mean()
img_std = img.std()
droplet_mask = ((img - img_mean) / img_std) > 2.5
max_slice = np.argmax(np.sum(img, axis=(1,2)))
plt.subplot(211)
plt.title(str(max_slice))
plt.imshow(img[max_slice])
plt.subplot(212)
plt.imshow(droplet_mask[max_slice])
plt.show()
print(img.shape)

label_img = measure.label(droplet_mask)
region_props = measure.regionprops(label_img, img)
region_props_2D = measure.regionprops(label_img[max_slice], img[max_slice])

integrated_intensities = np.zeros(len(region_props_2D))
volumes = np.zeros_like(integrated_intensities)
areas = np.zeros_like(integrated_intensities)

for i, prop in enumerate(region_props_2D):
    integrated_intensities[i] = img[max_slice][prop.coords].sum()
    areas[i] = prop.filled_area
    volumes[i] = region_props[prop.label - 1].filled_area

plt.scatter(volumes, integrated_intensities)
plt.show()
plt.scatter(areas, integrated_intensities)
plt.show()
plt.scatter(volumes, areas)
plt.show()


print()