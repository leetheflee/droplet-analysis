from skimage import io
from pathlib import Path
from PIL import Image
import numpy as np

input = Path('mEGFP-MED1-IDR 12% 300K/7')
out_dir = Path('input') / input.name

if not out_dir.exists():
    out_dir.mkdir()

all_file_prefixes = set(file.name.split('_T')[0] for file in input.glob("*.tif"))

for prefix in all_file_prefixes:
    img_sum = None
    num_imgs = 0
    for fil in input.glob(f'{prefix}_*.tif'):
        print(fil)
        img = io.imread(fil)
        num_imgs += 1
        if img_sum is None:
            img_sum = img.astype(float)
        else:
            img_sum += img
    mean_img = (img_sum / num_imgs).astype(np.uint8)
    im = Image.fromarray(mean_img)
    im.save(out_dir / f'{prefix}.tif')
