def get_entry(dict_, key, value):
    for entry in dict_:
        if entry[key] == value:
            return entry
    return {}
