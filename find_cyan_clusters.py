from PIL import Image
import numpy as np

img = Image.open('assets/textures/baked/miscBaked1024.png').convert('RGB')
arr = np.array(img)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# Find cyan pixels (typical neon cyan color range)
cyan = (r < 100) & (g > 150) & (b > 150)
ys, xs = np.where(cyan)

print(f"Total cyan pixels: {len(xs)}")
grid_size = 512
h, w = img.height, img.width

for y in range(0, h, grid_size):
    for x in range(0, w, grid_size):
        sub_cyan = cyan[y:y+grid_size, x:x+grid_size]
        count = np.sum(sub_cyan)
        if count > 500:
            print(f"Cyan cluster at x={x}-{x+grid_size}, y={y}-{y+grid_size}: count={count}")
            crop = img.crop((x, y, x+grid_size, y+grid_size))
            crop.save(f"misc_cyan_{x}_{y}.png")
