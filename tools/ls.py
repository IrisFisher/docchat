import json
import glob
from tools.is_path_safe import is_path_safe

def ls(folder=None):
    
    """Lists all of the files in a folder"""
    if is_path_safe(folder):
        try:
            if not folder:
                folder = None
            return sorted(glob.glob('*', root_dir=folder))
        except FileNotFoundError:
            return('Error: Folder not found.')