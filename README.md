# python_azure_function_step_2

The idea is to start with [this 'library' or python code base](https://github.com/sjondavey/python_azure_function_step_1) and apply the techniques from [Microsoft's beginner tutorial](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01), take an existing project and create Azure Function Endpoints and hook up Azure Blob Storage both to trigger the function and to store the results of the Monte Carlo Simulation (the analysis of those scenarios will not be detailed here).

Here I use Python 3 and develop in VSCode. Since I'm a noob, I'm documenting all the stuff I have to google to get up and running. 

Make sure you have installed all the necessary software and [configured your environnement](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python#configure-your-environment)

Step 1 contains no Azure, it is here as an example of an existing project (code base) that we will gradually evolve into an Azure native, serverless calculator using Azure Functions and Azure Blob Storage to perform Monte Carlo simulation and persist the simulated values for later (xVA type) analysis.

Target Project Structure (NB Azure Functions stuff at this point)
```
equityportfolioevolver  
├── .venv/                              # [Not in source control] Python Virtual Environment    
├── .vscode/                            # Local vscode environment variables  
│   ├── launch.json                     # To ensure we can run python from the project root  
│   └── settings.json                   # Settings to get unittest working correctly  
├── equityportfolioevolver/             # Folder for source files that will be deployed to Azure (so excludes testing for example)
│   ├── contracts/                      # Parent folder for groups of derivatives (called portfolios)  
│   │   └── portfolio.py                # Simple unmargined equity forwards (mostly hard coded)  
│   ├── rates/                          # Parent folder for rates environments  
│   │   └── rates_evolver.py            # Uncorrelated Brownian Motion with flat volatility and constant discount rates
├── test/                               # Test folder outside of source folder (will not be packaged and sent to Azure Functions)
│   ├── test_portfolio.py               # Tests for the portfolio code  
│   └── test_rates_evolver.py           # Tests for the rates evolver  
├── .gitignore                          # List of stuff not under source control  
└── requirements.txt                    # packages that are required and will need to be installed in Azure Functions to run your code  
```

### The virtual environment 
Virtual environments are required to ensure Azure can recreate a suitable environnement for the function
```python
python -m venv .venv
pip install numpy
pip install pandas
pip list                           # in case you are interested to see the packages in the virtual environment
pip freeze > requirements.txt      # create the file with installed packages
```

### Use the virtual environnement in VSCode 
[It is worth reading Microsoft's document](https://code.visualstudio.com/docs/python/environments) if you have not already done so. The trick is to ensure you have the last two lines of this `launch.json` file. The default version of this file created in the Microsoft document does not have this because it is not using the project structure I'm using.
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"PYTHONPATH": "${workspaceRoot}"},
            "cwd": "${workspaceFolder}"
        }
    ]
}
```
### Setting up VSCode for testing
I use unittest. [Microsoft has a document](https://code.visualstudio.com/docs/python/testing) well worth reading if you have not done so already.

From VSCode `Ctrl+Shft+P` and select `Python: Configure Tests`. I use `unittest Standard test framework`. The default setup of `settings.json` does not need to be changed.

Hopefully that is all you need to run the tests in VSCode (assuming obviously you have Python extension installed. I also use Pylance for linting)

