import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

# Let's inspect nodes
nodes = gltf.get('nodes', [])
meshes = gltf.get('meshes', [])

print("Nodes in GLTF:")
for idx, node in enumerate(nodes):
    name = node.get('name', '')
    mesh_idx = node.get('mesh')
    children = node.get('children', [])
    if 'jesse' in name.lower() or 'zhou' in name.lower():
        print(f"Node {idx}: name='{name}', mesh_index={mesh_idx}, children={children}")

print("\nMeshes in GLTF:")
for idx, mesh in enumerate(meshes):
    name = mesh.get('name', '')
    if 'jesse' in name.lower() or 'zhou' in name.lower():
        print(f"Mesh {idx}: name='{name}'")
