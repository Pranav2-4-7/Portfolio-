import json

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    gltf = json.load(f)

print("Nodes in GLTF:")
for idx, node in enumerate(gltf.get('nodes', [])):
    name = node.get('name', '')
    mesh = node.get('mesh')
    children = node.get('children', [])
    print(f"Node {idx:3d}: name='{name:25s}' mesh={mesh} children={children}")
