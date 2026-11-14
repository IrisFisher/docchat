from tools.is_path_safe import is_path_safe

def cat(file):
    #python -m doctest -v tools/cat.py
    """Opens a file and outpus its contents
    >>> cat('tools/test_file.txt')
    'this is a tester'
    """
    if is_path_safe(file):
        try:
            with open(file, encoding = 'utf-8') as f:
                return (f.read())
        except FileNotFoundError:
            return('Error: File not found.')
        except UnicodeDecodeError:
            return('Error: Could not decode file with utf-8')