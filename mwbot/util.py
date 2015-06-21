def null_func(*args, **kwargs):
    pass

def append_wrapper(list):
    """ Returns a decorator that appends its argument to 'list' """
    def decorator(x):
        list.append(x)
        return x
    return decorator

def append_name_wrapper(list):
    """ Returns a decorator that appends its argument's name to 'list' """
    def decorator(x):
        list.append(x.__name__)
        return x
    return decorator
