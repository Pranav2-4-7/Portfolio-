from PIL import Image
import numpy as np

print("Loading miscBaked1024.png...")
img = Image.open('assets/textures/baked/miscBaked1024.png').convert('RGB')
arr = np.array(img)
print("Loaded. Scanning...")

# We are looking for the sign board which has:
# - Neon pink (r > 180, g < 100, b > 150)
# - Or neon cyan (r < 100, g > 180, b > 180)
# - Or white (r > 200, g > 200, b > 200)
# let's find all pixels that match these neon colors
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
neon_pink = (r > 180) & (g < 100) & (b > 150)
neon_cyan = (r < 100) & (g > 180) & (b > 180)

# Find coordinates where these colors are clustered
ys_p, xs_p = np.where(neon_pink)
ys_c, xs_c = np.where(neon_cyan)

print(f"Neon pink range: x={ys_p.min()}-{ys_p.max()} y={xs_p.min()}-{xs_p.max()}")
print(f"Neon cyan range: x={ys_c.min()}-{ys_c.max()} y={xs_c.min()}-{xs_c.max()}")

# Let's save a crop of areas where neon pink and neon cyan overlap/are close
# We can find bounding box of cyan pixels:
x1, x2 = xs_c.min(), xs_c.max()
y1, y2 = ys_c.min(), ys_c.max()
print(f"Neon cyan bounding box: x={x1}-{x2}, y={y1}-{y2}")

# Let's divide this bounding box into chunks and save them
# We'll save a 1000x1000 crop around the cyan pixels
crop = img.crop((max(0, x1-50), max(0, y1-50), min(img.width, x2+50), min(img.height, y2+50)))
crop.save('cyan_region.png')
print("Saved cyan_region.png")
