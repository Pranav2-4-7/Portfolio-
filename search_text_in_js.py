import os

print("Searching for 'jesse' or 'zhou' in all files:")
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.js', '.html', '.css')):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    if 'jesse' in line.lower() or 'zhou' in line.lower():
                        print(f"  {path}:{line_num}: {line.strip()}")
