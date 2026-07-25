from PIL import Image
import numpy as np
import os

folder = 'assets/textures/baked'
for fname in os.listdir(folder):
    if not fname.endswith('.png'):
        continue
    path = os.path.join(folder, fname)
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    # Neon pink pattern search
    pink = (r > 150) & (g < 100) & (b > 130)
    ys, xs = np.where(pink)
    if len(xs) > 0:
        print(f"File {fname}: found pink pixels at x={xs.min()}-{xs.max()}, y={ys.min()}-{ys.max()} (count={len(xs)})")
        # Save a crop of the first bounding box of pink pixels
        crop = img.crop((max(0, xs.min()-10), max(0, ys.min()-10), min(img.width, xs.max()+10), min(img.height, ys.max()+10)))
        crop.save(f"pink_crop_{fname}")
    else:
        print(f"File {fname}: no pink pixels found.")
