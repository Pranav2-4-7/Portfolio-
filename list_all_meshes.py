import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

meshes = gltf.get('meshes', [])
print("All meshes in GLTF:")
for idx, mesh in enumerate(meshes):
    name = mesh.get('name', '')
    print(f"Mesh {idx:2d}: '{name}'")
