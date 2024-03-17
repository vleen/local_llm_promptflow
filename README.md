# Promptflow local template

The purpose of this project is to serve as a template for local LLM experimentation.

In the current iteration, the locally-stored model is loaded each time the flow is run. In the future this will be moved to a server that runs locally, so that the model is loaded only once and the Promtflow flow will just send requests to the local server.


# Setup and conventions

## Steps:


### 1. Conda environment setup

#### Loading the environment

There is a ```environment.yml```  file in the repository. Create your conda env by running:

```conda env create -f environment.yml```

*Note: the ```--from-history``` flag was omitted due to not including the right pip packages (including Promptflow). This could lead to cross-platform issues.*

#### Updating the environment

If you have installed/changed any packages in the provided environment and wish to update it so that others can run your code, export the updated environment definition by running the command:

```conda env export | grep -v -E "prefix|llama-cpp-python" > environment.yml```

And then add conda-force in the channels (after the default channels). The top of the ```environment.yml``` file should look like this:

```yml
name: llm_promptflow
channels:
  - defaults
  - conda-forge
  ...
dependencies:
  ...
```
### 2. Install ```llama-cpp-python``` in the conda environment

Activate the conda environment created in the previous step, then follow the [instructions here](https://github.com/abetlen/llama-cpp-python) to install ```llama-cpp-python``` according to your setup (e.g CPU/GPU, various backends etc).

For example, I have used the following command for my M1 Pro Mac:
```CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python```

**Remember to have the right conda environment activated when you install ```llama-cpp-python```!**

### 3. Install Promptflow VS Code extension

Search for "Promptflow" in the VS Code extension catalogue and install it.

### 4. Pre-commit hooks

Make sure the pre-commit hooks are installed before/if you start commiting to the repository. To do this, run ```pre-commit install``` in the root of the repo.


### 5. Get a local model

LLM model files (in ```.gguf``` format) are stored in the ```models/``` directory. The Promptflow flow takes the model names as parameters. Without these, there is no LLM to run.

Model files in ```.gguf``` format can be downloaded from HuggingFace. Currently, I am experimenting with ```codellama-13b-instruct.Q5_K_M.gguf``` from [here](https://huggingface.co/TheBloke/CodeLlama-13B-Instruct-GGUF).


