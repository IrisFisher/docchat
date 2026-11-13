import glob
import re

#python -m doctest -v tools/grep.py 

def grep(regex, path):
    """Returns every line in a set of files which matches a regular expression
    
    >>> grep('test','tools/*.txt')
    ['this is a tester']
    """
    

    try:
        assert path[0] != '/' or path != '..'
        result = []
        for file in glob.glob(path):
            with open(file, encoding = 'utf-8') as f:
                for line in f:
                    if re.search((regex),line) != None:
                        result.append(line)
        return result
    except FileNotFoundError:
        return('Error: File not found.')
    except UnicodeDecodeError:
        return('Error: Could not decode file with utf-8')
    except AssertionError:
        return('Sorry, you can not read files outside of the current folder.')