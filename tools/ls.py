import json
import glob

#with open("tools/tools.json", encoding='utf-8') as f:
    #tools = json.load(f)
    #print(tools)

def ls(folder=None):
    
    """Lists all of the files in a folder"""
    try:
        if not folder:
            folder = None
        return json.dumps({"result": sorted(glob.glob('*', root_dir=folder))})
    except FileNotFoundError:
        return('Error: Folder not found.')