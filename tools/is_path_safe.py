def is_path_safe(path):
    if path:
        try:
            assert (path[0] != '/') and ('..' not in path)
        except AssertionError:
            return False
    return True