from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Open original PNG
img = Image.open('assets/textures/baked/ramenShopBaked1024.png').convert('RGB')

# ─── The "Jesse's Ramen" neon sign is at: x=144-209, y=810-959 ─────────────
# It's rotated 90° clockwise in the UV map (text runs bottom-to-top)
# We'll paint this region with "PRANAV'S RAMEN"

sx1, sy1, sx2, sy2 = 143, 808, 211, 961  # sign bounds with 1px margin

# 1. Create a canvas the same size as the sign (rotated orientation)
sign_w = sx2 - sx1  # ~68px wide
sign_h = sy2 - sy1  # ~153px tall

sign_canvas = Image.new('RGB', (sign_h, sign_w), (6, 3, 15))  # dark bg, unrotated
sdraw = ImageDraw.Draw(sign_canvas)

# Neon border
sdraw.rectangle([2, 2, sign_h-3, sign_w-3], outline=(255, 45, 213), width=3)
# Inner glow border
sdraw.rectangle([6, 6, sign_h-7, sign_w-7], outline=(120, 20, 100), width=1)

# Text — "PRANAV'S RAMEN" split across two lines
# sign_canvas is (153 wide × 68 tall) in unrotated space
try:
    # Try to load a font
    font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
except:
    font_large = ImageFont.load_default()
    font_small = font_large

# Line 1: PRANAV'S
sdraw.text((sign_h//2, sign_w//2 - 10), "PRANAV'S", fill=(255, 255, 255),
           font=font_large, anchor='mm',
           stroke_fill=(255, 45, 213), stroke_width=1)
# Line 2: RAMEN
sdraw.text((sign_h//2, sign_w//2 + 10), "RAMEN", fill=(255, 200, 255),
           font=font_large, anchor='mm',
           stroke_fill=(255, 45, 213), stroke_width=1)

# 2. Rotate 90° CCW to match the UV orientation
sign_rotated = sign_canvas.rotate(90, expand=True)

# Verify sizes match
print(f"Sign region size: {sign_w}x{sign_h}")
print(f"Rotated canvas size: {sign_rotated.size}")

# 3. Paste into the main image
img.paste(sign_rotated, (sx1, sy1))

# Save verification crop (2x zoom for inspection)
verify = img.crop((sx1-20, sy1-20, sx2+20, sy2+20))
verify = verify.resize((verify.width*3, verify.height*3), Image.NEAREST)
verify.save('sign_result.png')
print("Saved sign_result.png for verification")

# 4. Save final modified texture as JPEG (used by the website)
img.save('assets/textures/baked/ramenShopBaked1024.jpg', 'JPEG', quality=95)
print("Saved modified ramenShopBaked1024.jpg ✓")
