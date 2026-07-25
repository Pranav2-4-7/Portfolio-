import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

accessors = gltf.get('accessors', [])
print(f"Total accessors: {len(accessors)}")
for idx in range(min(5, len(accessors))):
    print(f"Accessor {idx}: {accessors[idx]}")
