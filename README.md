# python_azure_function_step_2

The idea is to start with [this library or python code base](https://github.com/sjondavey/python_azure_function_step_1) and apply the techniques from [Microsoft's beginner tutorial](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01), take an existing project and create Azure Function Endpoints and hook up Azure Blob Storage both to trigger the function and to store the results of the Monte Carlo Simulation (the analysis of those scenarios will not be detailed here).

Here I use Python 3 and develop in VSCode. Since I'm a noob, I'm documenting all the stuff I have to google to get up and running. 

Make sure you have installed all the necessary software and [configured your environnement](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python#configure-your-environment)

### Turn this into an Azure Function Project
Using the Azure Extension in VSCode, select the `Create a new project` icon. Choose: Current directory, language = Python; HTTP trigger; function name I used is 'simulateEquityPortfolio'; Anonymous Authorization.

Now the Azure Extension is going to work its mojo. In particular it will ask to overwrite `requirements.txt` and `.gitignore`. Let it do this, we can fix this (regenerate `requirements.txt` and add back any specific items to `.gitignore`). By default the content of the new `requirements.txt` were not added to the projects virtual environment and I needed to do this manually `pip install azure-functions`. After this, regenerate the requirements with `pip freeze > requirements.txt` to get back all the packages used in the original project.

**Note:** 
1. At this stage there is no blob storage. We will run this as an HTTP trigger function and output the PFE.
2. Anonymous Authorization means this will be out 'in the wild' anyone can call it. Because there are people who 'just like to watch stuff burn' you should not leave your function exposed like this in Azure for any extended time. If the wrong person finds it and just decided to call it a lot, you could end up with a hefty bill. Since the chance this happens during dev and testing is small, I think it's fine for this stage.

The Azure function makes a lot of changes to the base project (see that project for file and folder descriptions). The project now looks like
Target Project Structure (NB Azure Functions stuff at this point)
```
equityportfolioevolver  
├── .venv/                              # [Not in source control] Added the Azure packages  
├── .vscode/                            # Local VScode environment variables  
│   ├── extensions.json                 # [new settings]
│   ├── tasks.json                      # [new settings]
│   ├── launch.json                     # Modified to include F5 functionality BUT needs to be changed (see below) 
│   └── settings.json                   # [unchanged]
├── equityportfolioevolver/             # [unchanged]
│   ├── contracts/                      # [unchanged]
│   │   └── portfolio.py                # [unchanged]
│   ├── rates/                          # [unchanged]
│   │   └── rates_evolver.py            # [unchanged]
├── simulateEquityPortfolio/            # Folder for everything that we will need for the Azure hooks
│   ├── __init__.py                     # By default, this is where the Azure call will start. It contains boilerplate code for a `hello world` type call
│   ├── function.json                   # Details of how the function is supposed to operate (eg http trigger, get and post methods etc)
│   └── sample.dat                      # ____I'm not sure about this yet
├── test/                               # [unchanged]
│   ├── test_portfolio.py               # [unchanged]
│   └── test_rates_evolver.py           # [unchanged]
├── .gitignore                          # Overwritten so if you had specific items in there, you may have to add them back
├── host.json                           # ____I'm not sure about this yet
├── proxies.json                        # ____I'm not sure about this yet
└── requirements.txt                    # Overwritten and missing the packages the original project required. File must be fixed for the deployment to work
```

### Change the default behaviour on launch
 In the initial project `launch.json` was set up so that pressing `F5` would run **the file that had focus in VSCode**. The Azure extension want F5 to fun the Azure Function locally (including emulating the server environnement). Until the original settings are deleted, `F5` will not run correctly. 

The original `launch.json` is in the README.md file for the first step. Turing this into an Azure Project appended to it. We must delete the original configuration now to ensure `F5` works are required for testing the function locally. When you have completed editing it, it should look as follows:
```
{
    "configurations": [
        {
            "name": "Attach to Python Functions",
            "type": "python",
            "request": "attach",
            "port": 9091,
            "preLaunchTask": "func: host start"
        }
    ]
}
```

Before creating any code, you should now do a quick test to make sure you can run the `hello world` boilerplate code. See the [Run the function locally](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python#configure-your-environment) section of the Microsoft configuration documentation. 

### Change how local functions are imported
[For reference see here.](https://github.com/Azure/azure-functions-python-worker/issues/219)

In the original `launch.json`, the project root was set as the path from which modules in the project would be imported. So for example in `portfolio.py` we used
```python
from equityportfolioevolver.rates.rates_evolver import RatesEvolver
```
Once we change `launch.json` we need to alter from these absolute (?) imports to relative imports. This line changes to the relative import
```python
from ..rates.rates_evolver import RatesEvolver
```
The tests classes do not need to be changed as their behaviour is governed by `settings.json`. Relative imports are also used in the helper code added in the function folder. For illustrative purposes the following files are added
```
equityportfolioevolver  
├── .venv/                              # [Not in source control] 
.
.
├── simulateEquityPortfolio/            # Folder for everything that we will need for the Azure hooks
│   ├── __init__.py                     # changed to call single_stock_mc.py and do something more than the basic hello world example
│   ├── function.json                   # [unchanged]
│   ├── sample.dat                      # [unchanged]
│   └── single_stock_mc.py              # make a simple call to the base python code
.
.
└── requirements.txt                    # [unchanged]
```
A call to this function is made from the web browser as 
```
http://localhost:7071/api/simulateEquityPortfolio?isin=something&long_short=long&volume=1000&strike=16.7&ttm=1.57
```

When you look at `__init__.py` you will see that it is also possible to pass the Function a JSON input. I was not able to set this up over the URL and needed to use [Postman](https://www.postman.com) to do this. In Postman a call can be sent passing the 
1. Parameters: Get call with the Params populated as key = isin; value = some_isin ...
2. JSON: Call with header / Content-Type set to application / json and then Body set to raw with the input
```
{
    "isin":"something",
    "long_short":"long",
    "volume":1000,
    "strike":16.7,
    "ttm":1.57
}
```
[See here for some documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-manually-run-non-http) which helped me get the JSON message working.
