def unpack(obj, attrs):
    ret = {}
    for key in attrs:
        ret[key] = getattr(obj, key)
    return ret

def unpack_many(obj, attrs):
    """ unpacks a List of Rows object into a List of Dicts
        obj = Listo of rows
        attrs = list of attributes to unpack """
    ret = []
    for i, row in enumerate(obj):
        ret.append({})
        for key in attrs:
            ret[i][key] = getattr(row, key)