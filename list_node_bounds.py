import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

nodes = gltf.get('nodes', [])
meshes = gltf.get('meshes', [])
accessors = gltf.get('accessors', [])

print("All node bounding boxes (using GLTF accessor metadata):")
for idx, node in enumerate(nodes):
    name = node.get('name', '')
    mesh_idx = node.get('mesh')
    
    # Get translation/rotation/scale if present
    trans = node.get('translation', [0, 0, 0])
    
    if mesh_idx is not None:
        mesh = meshes[mesh_idx]
        pos_acc_idx = None
        for prim in mesh.get('primitives', []):
            pos_acc_idx = prim.get('attributes', {}).get('POSITION')
            if pos_acc_idx is not None:
                break
        
        if pos_acc_idx is not None:
            acc = accessors[pos_acc_idx]
            min_pos = acc.get('min')
            max_pos = acc.get('max')
            if min_pos and max_pos:
                # Apply translation to centers
                center = [(min_pos[i] + max_pos[i])/2 + trans[i] for i in range(3)]
                print(f"Node {idx:3d}: '{name:22s}' (Mesh {mesh_idx:2d}) center={center} min={min_pos} max={max_pos}")
