"""Defines ls tool."""

import glob
from tools.is_path_safe import is_path_safe

def ls(folder=None):    
    #python -m doctest -v tools/ls.py
    """Lists all of the files in a folder
    >>> ls('tools')
    ['__init__.py', 'calculate.py', 'cat.py', 'grep.py', 'is_path_safe.py', 'ls.py', 'test_file.txt', 'test_photo.jpeg']
    >>> ls()
    ['README.md', '__init__.py', 'chat.py', 'pyproject.toml', 'requirements.txt', 'tools']
    """
    if is_path_safe(folder):
            if not folder:
                folder = None
            return sorted(glob.glob('*', root_dir=folder))