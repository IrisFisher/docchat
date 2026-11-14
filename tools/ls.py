import glob
from tools.is_path_safe import is_path_safe

def ls(folder=None):    
    #python -m doctest -v tools/ls.py
    """Lists all of the files in a folder
    >>> ls('tools')
    ['calculate.py', 'cat.py', 'grep.py', 'is_path_safe.py', 'ls.py', 'test_file.txt']
    """
    if is_path_safe(folder):
        try:
            if not folder:
                folder = None
            return sorted(glob.glob('*', root_dir=folder))
        except FileNotFoundError:
            return('Error: Folder not found.')