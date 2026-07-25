from PIL import Image, ImageDraw
import os

folder = 'assets/textures/baked'
for fname in os.listdir(folder):
    if fname.endswith('.png') or fname.endswith('.jpg'):
        path = os.path.join(folder, fname)
        try:
            img = Image.open(path).convert('RGB')
            w, h = img.size
            print(f"Texture: {fname} ({w}x{h})")
        except Exception as e:
            print(f"Failed to open {fname}: {e}")
