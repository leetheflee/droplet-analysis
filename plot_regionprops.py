from load import load_img, get_droplet_mask
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from itertools import chain
from tools import line_hist


working_directory = Path('input')
display = False
extensions = ['tif', 'czi']
min_area = 30
max_area = np.inf
n_std = 2

def droplet_area(props):
    return props.area

def droplet_integrated_intensity(props):
    return props.mean_intensity * props.area

prop_types = [
    ["Droplet area", droplet_area, {'range': (0, 1000)}],
    ["Integrated intensity per droplet", droplet_integrated_intensity, {'range': (0, 10)}]
]
 
property_results = {title: {} for title, func, hist_kwargs in prop_types}


for concentration_dir in working_directory.iterdir():
    concentration = float(concentration_dir.name)
    files = list(chain(*[concentration_dir.glob(f'*.{ext}') for ext in extensions]))

    for file in files:
        print(file)
        img = load_img(file, crop=1750, display=display)
#        img = subtract_off_mean_background_intensity(img)
        droplet_mask, region_props = get_droplet_mask(img, n_std, min_area, max_area)

        for props in region_props:
            for title, prop_func, hist_kwargs in prop_types:
                if not concentration in property_results[title]:
                    property_results[title][concentration] = []

                property_results[title][concentration].append(prop_func(props))

for title, prop_func, hist_kwargs in prop_types:
    results = property_results[title]
    for concentration, values in results.items():
        concentrations = np.full(len(values), concentration)
        line_hist(values, bins=20, normed=1, label=str(concentration), **hist_kwargs)
        plt.title(f"{title}, nstd={n_std}, min area={min_area}, max area={max_area}")
        plt.legend()

    plt.xlabel("HsTBP-IDR:YFP at 50mM KCl, 12% PEG")
    plt.show() 