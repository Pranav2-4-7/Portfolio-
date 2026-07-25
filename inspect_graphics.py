from PIL import Image

img = Image.open('assets/textures/baked/graphicsBaked512.png').convert('RGB')
img.save('verify_graphics.png')
print("Saved verify_graphics.png")
