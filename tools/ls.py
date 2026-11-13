import json
import glob
from is_path_safe import is_path_safe

#with open("tools/tools.json", encoding='utf-8') as f:
    #tools = json.load(f)
    #print(tools)

def ls(folder=None):
    
    """Lists all of the files in a folder"""
    if is_path_safe(folder):
        try:
            if not folder:
                folder = None
            return json.dumps({"result": sorted(glob.glob('*', root_dir=folder))})
        except FileNotFoundError:
            return('Error: Folder not found.')