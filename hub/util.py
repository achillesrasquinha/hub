import json

def get_if_empty(a, b):
    if not a:
        a = b
    return a

def safe_json_loads(*args):
    jsonified = [ ]

    for arg in args:
        try:
            arg = json.loads(arg)
        except Exception as e:
            pass
        jsonified.append(arg)
    
    return jsonified

def sequencify(arg):
    if not isinstance(arg, (list, tuple)):
        arg = [arg]
    return arg