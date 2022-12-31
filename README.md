# debug-decorator
Small Python Decorator tool for making debugging code easier

## Features:
1. Funtion names are outputed in the beginning and end of the debug wrapper with distinct visual cues.
2. Positional and Keyword Arguments passed into a debugged function are are grouped by type and listed.
3. If one debugged function is called from within another debugged function, it is visibly clear in the output.
4. Time taken for each function is displayed at the end of the wrap
5. Wrapper is sized to the size of the terminal.
6. Any type of variable can be passed and outputted to terminal (discord.Channel in the example)
7. Values that are too wide to fit in the terminal are automatically broken apart and made to fit.
8. If multiple functions are called in a chain, they appear in the other they were called (In the example all functions result from a single function). 

![image](https://user-images.githubusercontent.com/99280463/210119517-3db162ce-e4c5-4901-89e0-63510c6a07d4.png)

## How to use:
1. Add decorators.py to your project folder, for example under `./src/tools` as `decorators.py`
2. Import it as follows supposing you saved it to `./src/tools/decorators.py`
```py
import src.tools.decorators as debug
from src.tools.decorators import DEBUG
debug.DEBUG_ON = True
```
3. `debug.DEBUG_ON` is the "on/off" switch for the entire decorator.
4. DEBUG is the decorator itself and is what you will want to place before a function.
    Basic Example: To debug `myfunc(*args,**kwargs)` use:
      ```py
      @DEBUG()
      def myfunc(*args,**kwargs)
      ```
    This will result in the following in your terminal:
    1. When the function is called, it will be wrapped with `[function name] Started` and `[function name] Ended`.
    2. All Positional Arguments and Keyword Arguments passed into the function will be listed
    
    Advanced Example with different usage: To debug `myfunc(*args,**kwargs)` as well as variables within the inner function use:
      ```py
      @DEBUG()
      async def myfunc(*args,**kwargs):
        debug.KEY['var1'] = 'my string' # or any function that might set the string, for example:
        
        debug.KEY['final_url'] = base_url + query_part + id_part + instance_part
        final_url = debug.KEY['final_url']
        async with aiohttp.ClientSession() as session:
          async with session.get(final_url) as response:
            debug.KEY['response'] = str(await response.text())
            r = json.loads(debug.KEY['response'])
            
        debug.KEY['var2'] = 123
        debug.KEY['var3'] = ['a string','another string']
        .
        .
        .
        return debug.KEY['var1']
      ```
    This will result in the following in your terminal:
    1. When the function is called, it will be wrapped with `[function name] Started` and `[function name] Ended`.
    2. All Positional Arguments and Keyword Arguments passed into the function will be listed
    3. Each variable will be automatically exposed in your terminal, including both their name (var1,var2,var3,etc...) as well as the value of the variable.
