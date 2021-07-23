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
for salt_dir in working_directory.iterdir(): #iterate through directories in working directory
    # display = False or int(concentration_dir.name) > 0 #skips over directory labelled "0"
    salt_status = float(salt_dir.name) #gets name from directory name
    #if concentration in [0]:
       # continue
    files = list(chain(*[salt_dir.glob(f'*.{ext}') for ext in extensions])) #works with .tif and .czi files
    num_files[salt_status] = len(files)
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
            integrated_intensities[salt_status].append(integrated_intensity) #appends to dictionary defined in line 18 
            sizes[salt_status].append(prop.equivalent_diameter*2) #appends to dictionary defined in line 19, multiply to increase differences
            areas[salt_status].append(prop.area)

boxplot_median_props = {
    'c': 'black'
}

for salt_status, intensities in integrated_intensities.items():
    salt_statuss = np.full(len(intensities), salt_status)
    salt_statuss += np.clip(np.random.normal(0,0.1,size=salt_statuss.shape[0]), -0.2, 0.2)
    plt.plot()
    plt.scatter(salt_statuss, intensities, s=sizes[salt_status], alpha=0.1)
    plt.boxplot(intensities, positions=[salt_status], showfliers=False, widths=0.5, medianprops=boxplot_median_props)
    #plt.title('Integrated intensity per droplet for MED1-IDR in reponse to increasing nuclear extract concentrations')
    plt.title('Integrated intensity per droplet for PfRPB1-CTD in reponse to changing salt conditions at 12% PEG')
    plt.xlim(-1,5)
    #plt.xlabel('Nuclear extract concentration. 0=0.1, 1=0.125, 2=0.25')
    plt.xlabel('Salt status. 0=150mM KCl; 1=imm dilution, 150mM KCl; 2=imm dilution, 500mM KCl; 3=30min dilution, 150mM KCl;4=30min dilution, 500mM KCl;')
    plt.ylabel('Integrated intensity')
plt.show()