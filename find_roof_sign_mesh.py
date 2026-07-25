import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

nodes = gltf.get('nodes', [])
meshes = gltf.get('meshes', [])
accessors = gltf.get('accessors', [])

print("Searching for nodes near the horizontal roof sign (x ~ -4.75, y ~ 3.72, z ~ -1.8) in GLTF:")
found = False
for idx, node in enumerate(nodes):
    name = node.get('name', '')
    mesh_idx = node.get('mesh')
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
                center = [
                    (min_pos[0] + max_pos[0])/2 + trans[0],
                    (min_pos[1] + max_pos[1])/2 + trans[1],
                    (min_pos[2] + max_pos[2])/2 + trans[2]
                ]
                
                # Check spatial range:
                if -5.5 < center[0] < -4.0 and 3.0 < center[1] < 4.5 and -2.5 < center[2] < -1.0:
                    print(f"MATCH: Node {idx:3d}: '{name}' (Mesh {mesh_idx:2d}) center={center} min={min_pos} max={max_pos}")
                    found = True

if not found:
    print("No nodes found in the target spatial range. Let's print all nodes with their centers to check them:")
    for idx, node in enumerate(nodes):
        name = node.get('name', '')
        mesh_idx = node.get('mesh')
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
                    center = [
                        (min_pos[0] + max_pos[0])/2 + trans[0],
                        (min_pos[1] + max_pos[1])/2 + trans[1],
                        (min_pos[2] + max_pos[2])/2 + trans[2]
                    ]
                    print(f"Node {idx:3d}: '{name}' center={center}")
