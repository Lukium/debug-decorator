from os import get_terminal_size

DEBUG = True
DEBUG_WIDTH = get_terminal_size().columns

def debug(*decoratorargs, **decoratorkwargs):
    def decorator(function):
        global DEBUG, DEBUG_WIDTH        
        async def wrapper(*args, **kwargs):
            if DEBUG:
                print(f'\n╔{str("{:═^{}}").format(f" {function.__name__} Started ", DEBUG_WIDTH -2)}╗') # Creates a centered string ('^') padded with ═ (':═') of custom length ('inner {}')
                if args:
                    print(f' Positional Arguments:')
                    for x in args:
                        print(f' {str(x)}')
                if kwargs:
                    print(f' Keyword Arguments:')
                    for key, value in kwargs.items():
                        print(f' {str(key)}: {str(value)}')
                print(f'╠{str("{:═^{}}").format(f"", DEBUG_WIDTH -2)}╣')
            result = await function(*args, **kwargs, **decoratorkwargs)
            if DEBUG:
                for arg in decoratorkwargs:
                    print(f'{str(arg)}: {str(decoratorkwargs[arg])}')
                print(f'╠{str("{:═^{}}").format(f"", DEBUG_WIDTH -2)}╣')
                print(f'╚{str("{:═^{}}").format(f" {function.__name__} Ended ", DEBUG_WIDTH -2)}╝\n')
            return result
        return wrapper
    return decorator
