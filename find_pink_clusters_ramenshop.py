from PIL import Image
import numpy as np

img = Image.open('assets/textures/baked/ramenShopBaked1024.png').convert('RGB')
arr = np.array(img)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

pink = (r > 150) & (g < 100) & (b > 130)

grid_size = 64
h, w = img.height, img.width

for y in range(0, h, grid_size):
    for x in range(0, w, grid_size):
        sub_pink = pink[y:y+grid_size, x:x+grid_size]
        count = np.sum(sub_pink)
        if count > 50:
            print(f"RamenShop cluster at x={x}-{x+grid_size}, y={y}-{y+grid_size}: count={count}")
            crop = img.crop((x, y, x+grid_size, y+grid_size))
            crop.save(f"rs_pink_{x}_{y}.png")
