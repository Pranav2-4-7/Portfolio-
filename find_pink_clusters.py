from PIL import Image
import numpy as np

img = Image.open('assets/textures/baked/miscBaked1024.png').convert('RGB')
arr = np.array(img)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# Find pink pixels
pink = (r > 150) & (g < 100) & (b > 130)
ys, xs = np.where(pink)

print(f"Total pink pixels: {len(xs)}")
# Find clusters of pink pixels using simple grid division
grid_size = 512
h, w = img.height, img.width

for y in range(0, h, grid_size):
    for x in range(0, w, grid_size):
        sub_pink = pink[y:y+grid_size, x:x+grid_size]
        count = np.sum(sub_pink)
        if count > 200:
            print(f"Cluster at x={x}-{x+grid_size}, y={y}-{y+grid_size}: count={count}")
            # Save crop for inspection
            crop = img.crop((x, y, x+grid_size, y+grid_size))
            crop.save(f"misc_cluster_{x}_{y}.png")
