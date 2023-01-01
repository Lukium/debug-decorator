from datetime import datetime
from os import get_terminal_size
import sys

DEBUG_ON = True
DEBUG_LEVEL = 0
key = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_format(**kwargs):
    ""
    if 'string1' in kwargs:
        #string1: str = str(kwargs['string1']).replace('\n', '').replace('\r','').strip()
        string1: str = ' '.join(str(kwargs['string1']).split())
    if 'string2' in kwargs:
        #string2: str = str(kwargs['string2']).replace('\n', '').replace('\r','').strip()
        string2: str = ' '.join(str(kwargs['string2']).split()) #Sets the string and removes whitespace as well as line breaks and tabs
    format_type: str = kwargs['type']
    DEBUG_WIDTH = get_terminal_size().columns
    if format_type == 'function_start': # Use Type "function_start" for first line where a function starts
        print(f'\n╔{str("{:═^{}}").format(f" {string1.upper()} STARTED ", DEBUG_WIDTH -2)}╗')
    elif format_type == 'function_end': # Use Type "function_end" for first line where a function starts
        print(f'╚{str("{:═^{}}").format(f" {string1.upper()} ENDED ({string2} Secs.) ", DEBUG_WIDTH -2)}╝\n')
    elif format_type == 'variable':
        string = ''
        if 'string1' in locals():
            string1 = f'{bcolors.WARNING}{string1}{bcolors.ENDC}'
            string = string1
        if 'string2' in locals():
            if string == '':
                string = string2
            else:
                string = f'{string}: {string2}'        
        if len(string) > DEBUG_WIDTH - 4:
            chunks = [string[i:i+(DEBUG_WIDTH - 4 )] 
                for i in range(0, len(string), (DEBUG_WIDTH - 4))]
            chunk_count = 0
            for chunk in chunks:
                chunk_count += 1
                if chunk_count == 1:
                    print(f'║ {str("{: <{}}").format(chunk, DEBUG_WIDTH - 4 + 9)} ║')
                else:
                    print(f'║ {str("{: <{}}").format(chunk, DEBUG_WIDTH - 4)} ║')
        else:
            print(f'║ {str("{: <{}}").format(string, DEBUG_WIDTH - 4 + 9)} ║')
    elif format_type == 'blank_separator': # Use Type "blank_separator" for Positional Arguments Separator
        print(f'╠{str("{:═^{}}").format(f"", DEBUG_WIDTH -2)}╣')
    elif format_type == 'positionals_separator': # Use Type "positionals_separator" for Positional Arguments Separator
        print(f'╠{str("{:═^{}}").format(f" Positional Arguments: ", DEBUG_WIDTH -2)}╣')
    elif format_type == 'keywords_separator': # Use Type "keywords_separator" for Positional Arguments Separator
        print(f'╠{str("{:═^{}}").format(f" Keyword Arguments: ", DEBUG_WIDTH - 2)}╣')
    elif format_type == 'variables_separator': # Use Type "variables_separator" for Positional Arguments Separator
        print(f'╠{str("{:═^{}}").format(f" Debugged Variables & Inner Functions: ", DEBUG_WIDTH - 2)}╣')
    else:
        print(f'Error: Invalid Format Type')

def DEBUGALL(function): # Define the decorator function. It takes a single argument, 'function', which is the function to be decorated.
    """
    This function is a decorator that prints the names and values of all local variables in the decorated function.
    It does this by taking a snapshot of the function's frame object, which contains the local variables, and iterating over its names and values.

    The decorator function takes a single argument, 'function', which is the function to be decorated.
    The decorator returns a wrapper function, which takes an arbitrary number of positional arguments (*args) and an arbitrary number of keyword arguments (**kwargs).
    The wrapper function calls the decorated function with these arguments and returns its result.

    Before calling the decorated function, the wrapper function sets a temporary trace function that takes a snapshot of the decorated function's frame object on the first "call" event.
    It then restores the original trace function and calls the decorated function.

    After the decorated function has been called, the wrapper function iterates over the names and values of all local variables in the decorated function's frame object,
    ignoring the special arguments 'args' and 'kwargs'. It then prints the name and value of each local variable.
    Finally, the wrapper function deletes the snapshot of the decorated function's frame object and returns the result of the decorated function.
    """
    async def wrapper(*args, **kwargs): # Define the inner function 'wrapper'. It takes an arbitrary number of positional arguments (*args) and an arbitrary number of keyword arguments (**kwargs).
        
        trace = sys.gettrace() # Get the current trace function.

        if DEBUG_ON:            
            print_format(string1 = function.__name__, type = 'function_start')
            if args:
                print_format(type = 'positionals_separator')
                for i in range(len(args)):
                    print_format(string1 = f'#{i+1} ({str(type(args[i]).__name__)})', string2 = f'{str(args[i])}', type = 'variable')
                #for arg in args:
                #    print_format(string2 = f'{str(arg)}', type = 'variable')                
            if kwargs:
                print_format(type = 'keywords_separator')
                for arg in kwargs:
                    print_format(string1 = f'({str(type(arg).__name__)}) {str(arg)}', string2 = f'{str(kwargs[arg])}', type = 'variable')
            print_format(type = 'variables_separator')
            frame_snapshot = None # Initialize the variable 'frame' to None.
            elapsed_time = None # Initialize time variable to None

            def get_locals(_frame, name, arg): # Define a temporary trace function that will take a snapshot of the next frame on the next "call" event and save its _frame into frame variable                
                nonlocal elapsed_time
                nonlocal frame_snapshot # Declare 'frame' as a nonlocal variable.
                if name == 'call': # If this is the first "call" event
                    frame_snapshot = _frame # assign the value of '_frame' to 'frame'
                    sys.settrace(trace) # and set the trace function back to the original trace function.
                return trace # Return the trace function
                        
            sys.settrace(get_locals) # Replace current trace funtion with out temporary trace function, it will return to original after next call event
            t_start = datetime.now() # Start counting time to calculate elapsed time
        try:
            result = await function(*args, **kwargs) # Calls our decorated function, which should trigger the frame snapshot of itself, then return to original trace.
        finally:
            sys.settrace(trace) # Sets trace back to original in the event something goes wrong with the function
        
        if DEBUG_ON:
            t_end = datetime.now() # Finish counting time to calculate elapsed time
            for name, value in frame_snapshot.f_locals.items(): # Iterate over the names and values of all local variables in the decorated function
                if name != 'args' and name != 'kwargs' and name not in args and name not in kwargs: # Ignore the special arguments 'args' and 'kwargs'.
                    print_format(string1 = f'({frame_snapshot.f_locals[name].__class__.__name__}) {name}', string2 = f'{value}', type = 'variable')
                    #print(f'{name}: {value}') # Print the name and value of the local variable.            
            elapsed_time = round((t_end - t_start).total_seconds(), 3) # Calculate elapsed time and assign it to elapsed time variable
            print_format(string1 = function.__name__, string2 = elapsed_time, type = 'function_end')

            


            frame_snapshot = None # Set snapshot to none before deleting
            del frame_snapshot # Delete snapshot of frame now that we are done with it.

        return result
    return wrapper

def DEBUG(function):
    global DEBUG_ON
    async def wrapper(*args, **kwargs):            
        global key
        key = {}
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
            kwargs['debug'] = True
            kwargs['debug_level'] = DEBUG_LEVEL
        result = await function(*args, **kwargs)
        if DEBUG_ON:
            end_time = datetime.now()
            total_time = round((end_time - start_time).total_seconds(), 3)
            for arg in key:
                arg_string = f'{str(arg)}: {str(key[arg])}'
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
            key = {}
        return result
    return wrapper
