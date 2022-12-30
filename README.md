# debug-tools
Small Python Decorator tool for making debugging code easier

![image](https://user-images.githubusercontent.com/99280463/210117272-ca1b4b6a-efbc-4f51-b0e0-50aa49de9ae2.png)

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
      @DEBUG(var1='', var2=0, var3=[],...)
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
