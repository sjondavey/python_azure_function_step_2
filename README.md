# python_azure_function_step_2

In this Step 2, I start a generic piece of Python code [this library or python code base](https://github.com/sjondavey/python_azure_function_step_1) and apply the techniques from [Microsoft's beginner tutorial](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01), to expose this as an HTTP triggered Azure Function. In step 3, I will add a blob storage trigger. As per Step 1, I am using Python 3 and VSCode and documenting all the stuff I have to google to get up and running. If you have not looked at step 1, do yourself a favour and check out the Notes in that Readme.md file. The Notes are important.

Azure Functions in Visual Studio Code requires software and [environnement configuration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python#configure-your-environment) before you get started.

### Expose Python Library Functionality as an HTTP triggered Azure Function
Here I follow the the official [tutorial](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-02), noting things that are not documented there. 

**Note: Project Structure** You can read the official documentation about folder structure [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#folder-structure). Currently (Aug 2020) there is however an issue when trying to implement this with a non-trivial project (i.e. a project that requires libraries) in VSCode using the Azure Functions Extensions. Some details are documented in the [References and details](#project-structure-references) section at the end of this ReadMe. Here I just document what to do to get it to work.

Using the Azure Extension in VSCode, select the `Create a new project` icon. In the first step of that Macro, you are asked to choose a directory for the Azure Function. You **must** create the Function within the folder `python_azure_function_step_2\equityportfolioevolver`. For the remaining macro options, choose:
1. Language: Python;
2. Select Python Interpreter or full path: 'Skip virtual environment'
3. HTTP trigger
4. Function name I used is 'simulateEquityPortfolioHttp'
5. Anonymous Authorization.

**Note: Anonymous Authorization** means this will be out 'in the wild' anyone can call it. Because there are people who just want to watch stuff burn, you should not leave your function exposed like this in Azure for any extended time. If the wrong person finds it and just decided to call it a lot, you could end up with a hefty bill. Since the chance this happens during dev and testing is small, I think it's fine for this stage.

The Azure Extension makes around 12 changes to the project structure. 

The project now looks like:
```
python_azure_function_step_2  
├── .venv/                              # [Not in source control]  
├── .vscode/                            # Local VScode environment variables  
│   ├── extensions.json                 # [unchanged]
│   ├── launch.json                     # Added 'Attach to Python Functions' shortcut for debugging Function using F5 key
│   ├── tasks.json                      # New 
│   └── settings.json                   # Include Functions settings 
├── equityportfolioevolver/             # [unchanged]
│   ├── contracts/                      # [unchanged]
│   │   └── portfolio.py                # [unchanged]
│   ├── rates/                          # [unchanged]
│   │   └── rates_evolver.py            # [unchanged]
│   ├── simulateEquityPortfolioHttp/    # Folder corresponding to the Function name
│   │   ├── __init__.py                 # This is where the Azure call will start. It contains boilerplate code for a `hello world` type call
│   │   ├── function.json               # Details of how the function is supposed to operate (eg http trigger, get and post methods etc)
│   │   └── sample.dat                  # ____I'm not sure about this yet
|   ├── .funcignore
|   ├── .gitignore
|   ├── local.settings.json
|   ├── proxies.json
|   └── requirements.txt
├── test/                               # [unchanged]
│   ├── contracts/                      # [unchanged]
│   │   └── portfolio.py                # [unchanged]
│   └── rates/                          # [unchanged]
│       └── rates_evolver.py            # [unchanged]
├── .gitignore                          # [unchanged]
├── README.md                           # [unchanged]
└── requirements.txt                    # [unchanged]
```
**Note** the duplicate `requirements.txt` and `.gitignore` files under `equityportfolioevolver`. If We had selected a Python Interpreter in point 2, VSCode would also have created a `.venv` folder in this directory. 

To make the Function use the virtual environment at the parent level, add the following line to `settings.json`:
```
   "azureFunctions.pythonVenv": "..\\.venv",
```

The new `requirements.txt` is the one that is deployed to Azure so it should be updated with all the packages in that are needed for the library that are already in the old `requirements.txt`

### Change the default behaviour on run
In the initial project `launch.json` was set up so that pressing `F5` would run **the file that had focus in VSCode**. The Azure extension includes an option for F5 to fun the Azure Function locally (called 'Attach to Python Functions'). To switch the 'focused' functionality of `F5`, choose the Run Menu (`Ctrl+Shft+D`) on the left of VSCode. At the top of the Run Menu is a green arrow and a drop down list to toggle between the `F5` functionality. 
 
You should now do a quick test to make sure you can run the `hello world` boilerplate code created by the Azure Extension before modifying it to run library code. See the [Run the function locally](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python#configure-your-environment) section of the Microsoft configuration documentation. 

### Exposing the library to the function
At this stage we can create some hooks between the Azure Function (Functions use a lot of JSON, the library uses a lot of DataFrames so some conversions and some other code for illustrative purposes only have been placed in `stock_forwards_mc.py)`. `__init__.py` is also changed. Not for any particular reason other than demonstration, I want to change the entry point in this file from `main` to something else - in this case `simulate`. To do this requires adding the line `"entryPoint": "simulate",` to `function.json` so the start of that file looks like
```python
{
  "scriptFile": "__init__.py",
  "entryPoint": "simulate",
  "bindings": [
   ...
```
With these changes, the Azure Function can be run locally. A call to this function is made from the web browser as 
```
http://localhost:7071/api/simulateEquityPortfolioHttp?isin=something&long_short=long&volume=1000&strike=16.7&ttm=1.57
```

When you look at `__init__.py` you will see that it is also possible to pass the Function a JSON input. I was able to use [Postman](https://www.postman.com) to hit this part of the API call. In Postman a call can be sent passing the 
1. Parameters: Get call with the Params populated as key = isin; value = some_isin ...
2. JSON: POST message with Call with header / Content-Type set to application / json and then Body set to raw with the input
```
{"forwards":[
            {'isin': 'isin_1', 'long_short': 'long', 'volume': 1000, 'strike': 16.4, 'ttm': 1.52},
            {'isin': 'isin_2', 'long_short': 'short', 'volume': 500, 'strike': 12.3, 'ttm': 0.98}
            ]}
```
[See here for some documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-manually-run-non-http) which helped me get the JSON message working.

Finally the two test files `test_simulate_stock_portfolio.py` and `test_single_stock_mc.py` are added to the testing folder. The former shows how to construct HTTP Requests to test calls to the function using parameters and using a JSON body.


### Project Structure References
The start of a relevant discussion can be found [here](https://github.com/Azure/azure-functions-python-worker/issues/469) and [especially here](https://github.com/Azure/azure-functions-python-worker/issues/469#issuecomment-645164001). 

The issue is the need to expose the functions from within the `equityportfolioevolver` folder. The easiest way to do this [in VSCode](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-02) is to use the Azure (`ctr+-shft+A`) Extension and `Create New Project ...` option. To avoid issues with relative vs absolute imports, in the first step of that macro, you MUST `Browse` into the `python_azure_function_step_2\equityportfolioevolver` folder and then create the project there. The PROBLEM however is that the Azure Functions Extension will want to create a **new virtual environnement** inside `equityportfolioevolver`. If you follow some of the links referenced in this section, you will see that the original virtual environnement will be referred to as the 'dev-virtual environnement' and the new one (at the lower level) will be called the 'production virtual environment'. This just did not make a lot of sense to me. I just wanted 1 virtual environment. This is where [this comment](https://github.com/Azure/azure-functions-python-worker/issues/469#issuecomment-645164001) was essential. Make those chances to `settings.json` and `tasks.json` and then delete virtual environnement created by the Azure Functions Extension. Do note however that the new `requirements.txt` must remain.
