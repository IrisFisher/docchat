import json
import glob

#with open("tools/tools.json", encoding='utf-8') as f:
    #tools = json.load(f)
    #print(tools)

def ls(folder='*'):
    """Lists all of the files in a folder"""
    if not folder:
        folder = '*'
    print(folder)
    result = ''
    for name in sorted(glob.glob(folder)):
        result = result + name + '  '
    return json.dumps({"result": result})