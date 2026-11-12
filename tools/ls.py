import json
import glob

with open("tools/tools.json", encoding='utf-8') as f:
    tools = json.load(f)

def ls(folder='*'):
    """Lists all of the files in a folder"""
    if not folder:
        folder = '*'
    print(folder)
    result = ''
    for name in sorted(glob.glob(folder)):
        result = result + '\t' + name
    return json.dumps({"result": result})