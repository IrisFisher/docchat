def is_path_safe(path):
    """Checks if path is safe (inside current working repository)."""
    if path:
        try:
            assert (path[0] != '/') and ('..' not in path)
        except AssertionError:
            return False
    return True