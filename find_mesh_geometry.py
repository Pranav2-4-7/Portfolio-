import json
import numpy as np

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

nodes = gltf.get('nodes', [])
meshes = gltf.get('meshes', [])
accessors = gltf.get('accessors', [])
bufferViews = gltf.get('bufferViews', [])
buffers = gltf.get('buffers', [])

# Find binary data
import base64
bin_data = b''
for buf in buffers:
    uri = buf.get('uri', '')
    if uri.startswith('data:application/octet-stream;base64,'):
        bin_data += base64.b64decode(uri.split(',')[1])
    elif uri.startswith('data:image/'):
        pass
    elif uri:
        # load external file
        with open('assets/models/ramenShop/glTF/' + uri, 'rb') as f_bin:
            bin_data += f_bin.read()

def get_accessor_data(acc_idx):
    acc = accessors[acc_idx]
    bv_idx = acc.get('bufferView')
    if bv_idx is None:
        return np.array([])
    bv = bufferViews[bv_idx]
    offset = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    length = acc.get('count')
    # 5126 is FLOAT
    component_type = acc.get('componentType')
    dtype = np.float32 if component_type == 5126 else np.uint16
    stride = bv.get('byteStride', 0)
    
    num_components = 3 if acc.get('type') == 'VEC3' else 1
    bytes_per_element = 4 if dtype == np.float32 else 2
    element_size = num_components * bytes_per_element
    
    data = []
    for i in range(length):
        start = offset + i * (stride if stride else element_size)
        val = np.frombuffer(bin_data[start:start+element_size], dtype=dtype)
        data.append(val)
    return np.array(data)

# Let's check bounding box of each node/mesh
print("Checking node positions in GLTF:")
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
            pos_data = get_accessor_data(pos_acc_idx)
            if len(pos_data) == 0:
                continue
            pos_data_world = pos_data + np.array(trans)
            min_pos = pos_data_world.min(axis=0)
            max_pos = pos_data_world.max(axis=0)
            center = (min_pos + max_pos) / 2
            
            # Check if near the sign (x near -4 to -5, y near 3 to 4, z near -1 to -3)
            # Let's do a broad check first
            if -6.0 < center[0] < -3.0 and 2.0 < center[1] < 4.5 and -4.0 < center[2] < -1.0:
                print(f"Node {idx:3d}: '{name}' (Mesh {mesh_idx}) center={center} min={min_pos} max={max_pos}")
