import json
import numpy as np

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

nodes = gltf.get('nodes', [])

def get_node_transform(node_idx):
    node = nodes[node_idx]
    matrix = node.get('matrix')
    if matrix:
        m = np.array(matrix).reshape((4, 4), order='F')
        return m
    
    # Build matrix from T/R/S
    t = node.get('translation', [0, 0, 0])
    r = node.get('rotation', [0, 0, 0, 1])
    s = node.get('scale', [1, 1, 1])
    
    # Translation matrix
    T = np.eye(4)
    T[0:3, 3] = t
    
    # Scale matrix
    S = np.eye(4)
    S[0, 0] = s[0]
    S[1, 1] = s[1]
    S[2, 2] = s[2]
    
    # Rotation matrix (from quaternion r = [x, y, z, w])
    R = np.eye(4)
    x, y, z, w = r
    R[0, 0] = 1 - 2*y*y - 2*z*z
    R[0, 1] = 2*x*y - 2*z*w
    R[0, 2] = 2*x*z + 2*y*w
    R[1, 0] = 2*x*y + 2*z*w
    R[1, 1] = 1 - 2*x*x - 2*z*z
    R[1, 2] = 2*y*z - 2*x*w
    R[2, 0] = 2*x*z - 2*y*w
    R[2, 1] = 2*y*z + 2*x*w
    R[2, 2] = 1 - 2*x*x - 2*y*y
    
    return T @ R @ S

# Find parent-child relationships
parent_map = {}
for i, node in enumerate(nodes):
    for child_idx in node.get('children', []):
        parent_map[child_idx] = i

def get_absolute_transform(node_idx):
    path = [node_idx]
    curr = node_idx
    while curr in parent_map:
        curr = parent_map[curr]
        path.append(curr)
    
    # Multiply matrices from root to leaf
    M = np.eye(4)
    for idx in reversed(path):
        M = M @ get_node_transform(idx)
    return M

# Let's calculate absolute centers of the target meshes
for target_name in ['jesseZhouJoined', 'jZhouPink', 'jZhouBlack']:
    for idx, node in enumerate(nodes):
        if node.get('name') == target_name:
            M = get_absolute_transform(idx)
            # Extract absolute translation
            abs_t = M[0:3, 3]
            print(f"Absolute center for '{target_name}': {abs_t}")
