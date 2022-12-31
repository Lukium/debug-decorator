from datetime import datetime
from os import get_terminal_size

DEBUG_ON = True
KEY = {}

def DEBUG(**decoratorkwargs):    
    def decorator(function):
        global DEBUG_ON
        async def wrapper(*args, **kwargs):            
            global KEY
            KEY = decoratorkwargs
            DEBUG_WIDTH = get_terminal_size().columns
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
                print(f'╠{str("{:═^{}}").format(f" Debugged Variables & Inner Functions: ", DEBUG_WIDTH - 2)}╣')
                start_time = datetime.now()
            result = await function(*args, **kwargs)
            if DEBUG_ON:
                end_time = datetime.now()
                total_time = round((end_time - start_time).total_seconds(), 3)
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
                print(f'╚{str("{:═^{}}").format(f" {function.__name__} Ended ({total_time} Secs.) ", DEBUG_WIDTH -2)}╝\n')
                total_time = 0
                KEY = {}
            return result
        return wrapper
    return decorator
