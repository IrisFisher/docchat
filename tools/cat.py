import json

def cat(file):
    """Opens a file and outpus its contents"""
    try:
        with open(file, encoding = 'utf-8') as f:
            return(f.read())
    except FileNotFoundError:
        return('Error: File not found.')
    except UnicodeDecodeError:
        return('Error: Could not decode file with utf-8')