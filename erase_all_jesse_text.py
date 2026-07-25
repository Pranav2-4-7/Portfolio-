from PIL import Image, ImageDraw

# Open original PNG texture
img = Image.open('assets/textures/baked/ramenShopBaked1024.png').convert('RGB')
draw = ImageDraw.Draw(img)

# The vertical sign panel runs from x=144 to x=210, and y=805 to y=962
# Let's paint the entire vertical panel with the dark sign background color (8, 4, 20)
# to completely erase "JESSE'S" at the top and "RAMEN" at the bottom.
draw.rectangle([143, 804, 211, 963], fill=(8, 4, 20))

# Save the updated PNG
img.save('assets/textures/baked/ramenShopBaked1024.png')

# Save the updated JPG (which is loaded by the site)
img.save('assets/textures/baked/ramenShopBaked1024.jpg', 'JPEG', quality=95)
print("Erazed all Jesse text from texture successfully!")

# Save a crop to verify
crop = img.crop((130, 800, 230, 970))
crop.save('verify_vertical_erased.png')
print("Saved verify_vertical_erased.png")
