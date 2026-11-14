"""Defines grep tool."""

import glob
import re
from tools.is_path_safe import is_path_safe

def grep(regex, path):
    #python -m doctest -v tools/grep.py 
    """Returns every line in a set of files which matches a regular expression
    
    >>> grep('test','tools/*.txt')
    ['this is a tester']
    """
    
    if is_path_safe(path):
        result = []
        for file in glob.glob(path):
            with open(file, encoding = 'utf-8') as f:
                for line in f:
                    if re.search((regex),line) != None:
                        result.append(line)
        return result