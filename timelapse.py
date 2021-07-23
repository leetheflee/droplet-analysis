from load import get_droplet_mask, load_img
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path

n_std = 2
STEP_SIZE = 30
X_START = 60

working_directory = Path('/mnt/c/Users/Leo/Google Drive/..Uni/Masters/Droplet analysis/droplet_analysis_Wilkinson/settle_2021.04.05_input')

times = []
condensed_fraction_areas = []

for file in working_directory.glob('*.tif'):
    print(file)
    img = load_img(file, crop=1750, display = False)
    droplet_mask, props = get_droplet_mask(img, n_std, 0, np.inf)
    times.append(int(file.name[9:12]) / 4 * 30 + 44.87 )
    #times.append(int(file.name[4:7]) / 10 * STEP_SIZE + X_START )
    condensed_fraction_areas.append(np.mean(droplet_mask))
    # condensed_fraction_areas.append(len(props))
    print(f"proportion of image droplet: {condensed_fraction_areas[-1]}")

plt.scatter(np.asarray(times), condensed_fraction_areas)
plt.ylim(0, np.max(condensed_fraction_areas)+0.02)
plt.xlabel("time (s)")
plt.ylabel("condensed fraction")
plt.title("Droplet settling over time")
plt.show()