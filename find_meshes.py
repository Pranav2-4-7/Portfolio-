import json, re

with open('assets/models/ramenShop/glTF/ramenShop.gltf', 'r') as f:
    content = f.read()

# Find all mesh names
names = re.findall(r'"name":\s*"([^"]+)"', content)

print('ALL names found in GLTF:')
for n in sorted(set(names)):
    print(' -', n)
