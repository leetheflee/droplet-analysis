from load import load_img, get_droplet_mask
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict
from itertools import chain


n_std = 2 #make arbitralily large to calcuate total intensity of image
min_area = 10
working_directory = Path('input')
extensions = ['tif', 'czi']

background_intensities = defaultdict(list)
num_files = defaultdict(list)
for concentration_dir in working_directory.iterdir():
    concentration = float(concentration_dir.name)
    files = list(chain(*[concentration_dir.glob(f'*.{ext}') for ext in extensions]))
    num_files[concentration] = len(files)
    for file in files:
        print(file)
        img = load_img(file, crop=1750, display = False)
        droplet_mask, props = get_droplet_mask(img, n_std, min_area, 3000)
        print(f"proportion of image droplet: {np.mean(droplet_mask)}")
        background_intensity = np.mean(img[~droplet_mask])
        background_intensities[concentration].append(background_intensity)

for concentration, intensities in background_intensities.items():
    concentrations = np.full_like(intensities, concentration)
    plt.scatter(concentrations, intensities)

plt.title(f"Background image intensity vs concentration, nstd= {n_std}, min area={min_area}")
plt.xlabel("mC:PfCTD P2 concentration at 150mM KCl")
plt.ylabel("Total image brightness")
plt.show()