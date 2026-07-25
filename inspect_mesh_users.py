import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

nodes = gltf.get('nodes', [])
mesh_to_nodes = {}
for idx, node in enumerate(nodes):
    mesh = node.get('mesh')
    if mesh is not None:
        if mesh not in mesh_to_nodes:
            mesh_to_nodes[mesh] = []
        mesh_to_nodes[mesh].append((idx, node.get('name', '')))

for mesh, node_list in sorted(mesh_to_nodes.items()):
    if len(node_list) > 1:
        print(f"Mesh {mesh} is used by multiple nodes: {node_list}")
    else:
        print(f"Mesh {mesh} used by: {node_list}")
