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
Manually change `launch.json`: The initial project was set up so that pressing `F5` would run **the file that had focus in VSCode**. The Azure extension want F5 to fun the Azure Function locally (including emulating the server environnement). Until the original settings are deleted, `F5` will not run correctly. 

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


