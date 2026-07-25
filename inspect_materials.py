import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

meshes = gltf.get('meshes', [])
materials = gltf.get('materials', [])

def inspect_mesh(idx, name):
    if idx < len(meshes):
        mesh = meshes[idx]
        print(f"Mesh {idx} ('{name}'):")
        for p_idx, prim in enumerate(mesh.get('primitives', [])):
            mat_idx = prim.get('material')
            mat_name = materials[mat_idx].get('name', '') if mat_idx is not None else 'None'
            print(f"  Primitive {p_idx}: material_index={mat_idx} ('{mat_name}')")

inspect_mesh(1, 'jesseZhouJoined')
inspect_mesh(32, 'jZhouPink')
inspect_mesh(41, 'jZhouBlack')
inspect_mesh(3, 'ramenShopJoined')
