

import json
with open('./CP/output.json', 'r',  encoding="utf-8") as f:
    data = json.load(f)
print(data)