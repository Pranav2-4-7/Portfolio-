import re, os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.js'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                matches = re.findall(r'[\'"][^\'"]+\.(?:gltf|glb)[\'"]', content)
                if matches:
                    print(f"File {path} references models:")
                    for m in matches:
                        print(f"  - {m}")
