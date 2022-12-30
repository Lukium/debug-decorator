from os import get_terminal_size

DEBUG_ON = True
DEBUG_WIDTH = get_terminal_size().columns
KEY = {}

def DEBUG(**decoratorkwargs):
    def decorator(function):
        global DEBUG_ON, DEBUG_WIDTH
        async def wrapper(*args, **kwargs):
            global KEY
            KEY = decoratorkwargs
            if DEBUG_ON:
                print(f'\n╔{str("{:═^{}}").format(f" {function.__name__} Started ", DEBUG_WIDTH -2)}╗') # Creates a centered string ('^') padded with ═ (':═') of custom length ('inner {}')
                if args:
                    print(f'╠{str("{:═^{}}").format(f" Positional Arguments: ", DEBUG_WIDTH -2)}╣')
                    for arg in args:
                        arg_string = f'{str(arg)}'
                        if len(arg_string) > DEBUG_WIDTH - 4:
                            chunks = [arg_string[i:i+(DEBUG_WIDTH - 4)] 
                                for i in range(0, len(arg_string), (DEBUG_WIDTH - 4))]
                            for chunk in chunks:
                                print(f'║ {str("{: <{}}").format(chunk, DEBUG_WIDTH - 4)} ║')
                        else:
                            print(f'║ {str("{: <{}}").format(arg_string, DEBUG_WIDTH - 4)} ║')
                if kwargs:
                    print(f'╠{str("{:═^{}}").format(f" Keyword Arguments: ", DEBUG_WIDTH - 2)}╣')
                    for arg, value in kwargs.items():
                        arg_string = f'{str(arg)}: {str(value)}'
                        if len(arg_string) > DEBUG_WIDTH - 4:
                            chunks = [arg_string[i:i+(DEBUG_WIDTH - 4)] 
                                for i in range(0, len(arg_string), (DEBUG_WIDTH - 4))]
                            for chunk in chunks:
                                print(f'║ {str("{: <{}}").format(chunk, DEBUG_WIDTH - 4)} ║')
                        else:
                            print(f'║ {str("{: <{}}").format(arg_string, DEBUG_WIDTH - 4)} ║')
                print(f'╠{str("{:═^{}}").format(f"", DEBUG_WIDTH - 2)}╣')
            result = await function(*args, **kwargs)
            if DEBUG_ON:
                for arg in KEY:
                    arg_string = f'{str(arg)}: {str(KEY[arg])}'
                    if len(arg_string) > DEBUG_WIDTH - 4:
                        chunks = [arg_string[i:i+(DEBUG_WIDTH - 4)] 
                            for i in range(0, len(arg_string), (DEBUG_WIDTH - 4))]
                        for chunk in chunks:
                            print(f'║ {str("{: <{}}").format(chunk, DEBUG_WIDTH - 4)} ║')
                    else:
                        print(f'║ {str("{: <{}}").format(arg_string, DEBUG_WIDTH - 4)} ║')
                print(f'╠{str("{:═^{}}").format(f"", DEBUG_WIDTH -2)}╣')
                print(f'╚{str("{:═^{}}").format(f" {function.__name__} Ended ", DEBUG_WIDTH -2)}╝\n')
                KEY = {}
            return result
        return wrapper
    return decorator
