from inspect import getmembers, getargspec


def get_functions_from_module(module):
    functions = []
    for op in getmembers(module):
        name, func = op[0], op[1]
        if callable(func):
            functions.append(func)
    return functions


def num_args_for_function(functions):
    function_and_num_args = []
    names = []
    for func in functions:
        try:
            name = func.__name__
            num_args = len(getargspec(func).args)
            item = (name, func, num_args)
            if name not in names and num_args > 0:
                names.append(name)
                function_and_num_args.append(item)
        except Exception as e:
            print(func, e)
    return function_and_num_args


