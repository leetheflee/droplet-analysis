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
min_area = 10
max_area = np.inf

integrated_intensities = defaultdict(list)
sizes = defaultdict(list)
areas = defaultdict(list)
num_files = defaultdict(list)
for hex_concentration_dir in working_directory.iterdir(): #iterate through directories in working directory
    # display = False or int(concentration_dir.name) > 0 #skips over directory labelled "0"
    hex_concentration = float(hex_concentration_dir.name) #gets name from directory name
    #if concentration in [0]:
       # continue
    files = list(chain(*[hex_concentration_dir.glob(f'*.{ext}') for ext in extensions])) #works with .tif and .czi files
    num_files[hex_concentration] = len(files)
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
            integrated_intensities[hex_concentration].append(integrated_intensity) #appends to dictionary defined in line 18 
            sizes[hex_concentration].append(prop.equivalent_diameter*2) #appends to dictionary defined in line 19, multiply to increase differences
            areas[hex_concentration].append(prop.area)

boxplot_median_props = {
    'c': 'black'
}

for hex_concentration, intensities in integrated_intensities.items():
    hex_concentrations = np.full(len(intensities), hex_concentration)
    hex_concentrations += np.clip(np.random.normal(0,2,size=hex_concentrations.shape[0]), -1, 1)
    plt.plot()
    plt.scatter(hex_concentrations, intensities, s=sizes[hex_concentration], alpha=0.1)
    plt.boxplot(intensities, positions=[hex_concentration], showfliers=False, widths=4, medianprops=boxplot_median_props)
    plt.title('Integrated intensity per droplet for PfRPB1-CTD at 12%, 150mM KCl')
    plt.xlim(-5,400)
    plt.xlabel('Hexanediol concentration')
    plt.ylabel('Integrated intensity')
plt.show()