from load import get_droplet_mask, load_img
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path
from tools import subtract_off_mean_background_intensity


working_directory = Path('/mnt/c/Users/Leo/Google Drive/..Uni/Masters/Droplet analysis/droplet_analysis_Wilkinson/input')
display = 0
nstd = 2
min_area = 5
max_area = np.inf

condensed_fractions = defaultdict(list)


for concentration_dir in working_directory.iterdir():
    concentration = float(concentration_dir.name)
    for file in concentration_dir.glob('*.tif'):
        print(file)
        img = load_img(file, crop=1750, display = display)
        droplet_mask, props = get_droplet_mask(img, nstd, min_area, max_area)
        print(f"proportion of image droplet: {np.mean(droplet_mask)}")
        condensed_fraction = np.mean(droplet_mask)
        condensed_fractions[concentration].append(condensed_fraction)

total_integrated_intensity_stds = []
concentrations, im_condensed_fractions = zip(*condensed_fractions.items())
condensed_fraction_means = [np.mean(fractions) for fractions in im_condensed_fractions]
condensed_fraction_stds = [np.std(fractions) for fractions in im_condensed_fractions]


plt.errorbar(concentrations, condensed_fraction_means, yerr=condensed_fraction_stds, linestyle='none', marker='o')
plt.title(f"mC-MED1-IDR at 12% PEG nstd= {nstd}, min area={min_area}, max area={max_area}")
plt.xlabel("KCl concentration (mM)")
plt.ylabel("Condensed fraction")
plt.ylim(0)
plt.show()

for concentration, fractions in condensed_fractions.items():
    concentrations = np.full(len(fractions), concentration)
    plt.scatter(concentrations, fractions, alpha=1)
plt.title(f"PfTFIIA-IDR E2 at 300mM KCl, nstd= {nstd}, min area={min_area}, max area={max_area}")
plt.xlabel("Relative PfTFIIA-IDR concentration")
plt.ylabel("Condensed fraction")
plt.ylim(0)
plt.show()

print()