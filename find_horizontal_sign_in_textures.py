from PIL import Image
import numpy as np

for name in ['miscBaked1024', 'machinesBaked1024', 'floorBaked1024', 'graphicsBaked512', 'ramenShopBaked1024']:
    img_path = f"assets/textures/baked/{name}.png"
    print(f"Scanning {img_path}...")
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    # Sign board background color is dark blue (approx R=8, G=4, B=20, or very dark)
    # Let's search for pixels with R < 20, G < 20, B < 40
    dark_blue = (r < 25) & (g < 25) & (b > 5) & (b < 45)
    
    # We are looking for a cluster of these dark blue pixels that has:
    # - Width > 150
    # - Height > 30
    # Let's do a sliding window search or find bounding boxes of connected components
    # Using scipy label:
    from scipy.ndimage import label
    labeled, num_features = label(dark_blue)
    print(f"  Found {num_features} dark blue regions.")
    for i in range(1, min(20, num_features + 1)):
        region = (labeled == i)
        ys, xs = np.where(region)
        if len(xs) == 0: continue
        w_region = xs.max() - xs.min()
        h_region = ys.max() - ys.min()
        if w_region > 100 and h_region > 20:
            print(f"  Region {i}: x={xs.min()}-{xs.max()} y={ys.min()}-{ys.max()} size={w_region}x{h_region}")
            crop = img.crop((max(0, xs.min()-10), max(0, ys.min()-10), min(img.width, xs.max()+10), min(img.height, ys.max()+10)))
            crop.save(f"detected_{name}_region_{i}.png")
            print(f"    Saved detected_{name}_region_{i}.png")
