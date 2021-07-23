from load import get_droplet_mask, load_img
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path
from tools import subtract_off_mean_background_intensity
from itertools import chain
from tools import line_hist

working_directory = Path('input')
extensions = ['tif', 'czi']

display = 0
nstd = 2
min_area = 5
max_area = 1000

integrated_intensities = defaultdict(list)
sizes = defaultdict(list)
partition_coefficients = defaultdict(list)
areas = defaultdict(list)
volumes = defaultdict(list)
total_integrated_intensity = defaultdict(list)
total_integrated_intensity_stds = defaultdict(list)
num_files = defaultdict(list)
for concentration_dir in working_directory.iterdir(): #iterate through directories in working directory
    # display = False or int(concentration_dir.name) > 0 #skips over directory labelled "0"
    concentration = float(concentration_dir.name) #gets name from directory name
    #if concentration in [0]:
       # continue
    files = list(chain(*[concentration_dir.glob(f'*.{ext}') for ext in extensions])) #works with .tif and .czi files
    num_files[concentration] = len(files)
    for file in files:
        print(file)
        img = load_img(file, crop=1750) #use crop to remove scale bar if present
        #img = subtract_off_mean_background_intensity(img) #not properly integrated functionality
        droplet_mask, props = get_droplet_mask(img, nstd, min_area, max_area) #uses function defined in "load" to get droplet mask, set parameters
        if display: #display image and mask side by side
            plt.subplot(121)
            plt.imshow(img)
            plt.subplot(122)
            plt.imshow(droplet_mask)
            plt.show()
        img_background_mean = np.mean(img[~droplet_mask]) #calculate mean of NOT droplet area
        for prop in props: #different properties of droplet mask regions
            integrated_intensity = np.sum(img[prop.coords[:,0],prop.coords[:,1]]) #sums pixel brightness values for each region
            integrated_intensities[concentration].append(integrated_intensity) #appends to dictionary defined in line 18 
            sizes[concentration].append(prop.equivalent_diameter*2) #appends to dictionary defined in line 19, multiply to increase differences
            partition_coefficient = np.mean(img[prop.coords[:,0],prop.coords[:,1]]) / img_background_mean
            partition_coefficients[concentration].append(partition_coefficient)
            areas[concentration].append(prop.area)
            volumes[concentration].append(4 / 3 * np.pi * (prop.equivalent_diameter/2)**3)

for concentration, intensities in integrated_intensities.items():
    total_integrated_intensity[concentration] = np.sum(intensities) / num_files[concentration]

boxplot_median_props = {
    'c': 'black'
}

boxplotwidths = 1.5
leftbound = 0
rightbound = 125
scatterwidth = 0.5
x_label = "PEG-3000 concentration (%)"

for concentration, intensities in integrated_intensities.items():
    concentrations = np.full(len(intensities), concentration)
    concentrations += np.clip(np.random.normal(0,2,size=concentrations.shape[0]), -scatterwidth, scatterwidth)
    plt.subplot(221)
    plt.scatter(concentrations, intensities, s=sizes[concentration], alpha=0.1)
    plt.boxplot(intensities, positions=[concentration], showfliers=False, widths=boxplotwidths, medianprops=boxplot_median_props)
    plt.title('Integrated intensity per droplet')
    plt.xlim(leftbound,rightbound)
    plt.xlabel(x_label)
    plt.ylabel('Integrated intensity')
    plt.subplot(222)
    plt.scatter(concentrations, partition_coefficients[concentration], alpha=0.5)
    plt.boxplot(partition_coefficients[concentration], positions=[concentration], showfliers=True, widths=boxplotwidths, medianprops=boxplot_median_props)
    plt.title('Partition coefficient per droplet')
    plt.xlim(leftbound,rightbound)
    plt.xlabel(x_label)
    plt.ylabel('Partition coefficient')
    plt.subplot(223)
    plt.scatter(concentrations, areas[concentration], alpha=0.1) 
    plt.boxplot(areas[concentration], positions=[concentration], showfliers=False, widths=boxplotwidths, medianprops=boxplot_median_props)
    plt.title('Droplet sizes')
    plt.xlim(leftbound,rightbound)
    plt.xlabel(x_label)
    plt.ylabel(r'Droplet area (${px}^2$)')
    plt.subplot(224)
    plt.scatter(concentrations, volumes[concentration])
    plt.boxplot(volumes[concentration], positions=[concentration], showfliers=False, widths=boxplotwidths, medianprops=boxplot_median_props)
    plt.title('Apparent droplet volumes')
    plt.xlim(leftbound,rightbound)
    plt.xlabel(x_label)
    plt.ylabel(r'Droplet volume (${px}^3$)')

plt.savefig('tmp.png')
plt.show()

total_integrated_intensity_stds = []
concentrations, total_intensities = zip(*total_integrated_intensity.items())

plt.errorbar(concentrations, total_intensities, linestyle='none', marker='o')
plt.show()
