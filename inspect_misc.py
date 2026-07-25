from PIL import Image
import numpy as np
import os

img = Image.open('assets/textures/baked/miscBaked1024.png').convert('RGB')
arr = np.array(img)

# Search for pink/magenta pixels in miscBaked1024.png (4096x4096)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
pink = (r > 150) & (g < 100) & (b > 130)

ys, xs = np.where(pink)
if len(xs) > 0:
    print(f"miscBaked1024.png pink range: x={xs.min()}-{xs.max()}, y={ys.min()}-{ys.max()}")
    # Let's save 4 different sub-crops of pink regions to inspect
    # Divide the bounding box into quadrants or check where density is high
    w, h = xs.max() - xs.min(), ys.max() - ys.min()
    
    # Save a few specific crops
    # Crop 1: top-left of pink region
    c1 = img.crop((xs.min(), ys.min(), xs.min() + min(1000, w), ys.min() + min(1000, h)))
    c1.save('misc_pink_1.png')
    
    # Crop 2: bottom-right of pink region
    c2 = img.crop((max(0, xs.max() - 1000), max(0, ys.max() - 1000), xs.max(), ys.max()))
    c2.save('misc_pink_2.png')
    
    # Crop 3: middle of pink region
    cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
    c3 = img.crop((cx - 500, cy - 500, cx + 500, cy + 500))
    c3.save('misc_pink_3.png')
    
    print("Saved misc_pink_1.png, misc_pink_2.png, misc_pink_3.png")
else:
    print("No pink found in miscBaked1024.png")
