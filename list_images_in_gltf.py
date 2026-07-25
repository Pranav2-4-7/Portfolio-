import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

images = gltf.get('images', [])
print("Images referenced in GLTF:")
for idx, img in enumerate(images):
    print(f"Image {idx}: {img.get('uri')}")
