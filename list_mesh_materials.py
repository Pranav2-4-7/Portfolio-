import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

meshes = gltf.get('meshes', [])
materials = gltf.get('materials', [])

print("GLTF Meshes and Materials:")
for idx, mesh in enumerate(meshes):
    name = mesh.get('name', '')
    prims = mesh.get('primitives', [])
    mat_names = []
    for p in prims:
        mat_idx = p.get('material')
        if mat_idx is not None:
            mat_names.append(materials[mat_idx].get('name', ''))
        else:
            mat_names.append('None')
    print(f"Mesh {idx:2d} ('{name}'): primitives material names={mat_names}")
