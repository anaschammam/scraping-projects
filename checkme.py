def check_key_exists(data, key):
    """
    Check if a key exists in a nested JSON object
    """
    if isinstance(data, dict):
        return key in data.keys() or any(check_key_exists(v, key) for v in data.values())
    elif isinstance(data, list):
        return any(check_key_exists(v, key) for v in data)
    return False
