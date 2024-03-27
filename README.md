# Promptflow local template

The purpose of this project is to serve as a template for local LLM experimentation using Promptflow.

The repo contains two Promptflow flows:

- ```local_codellama_flow``` -  naively loads a local model file each time it runs (i.e. simplest & most inefficient).
- ```local_server_codellama_flow``` -  uses a local server to host the LLM.

---

# Initial setup steps

## 1. Conda environment setup

### Creating the environment

There is a ```environment.yml```  file in the repository. 

Note that there is a ```llama-cpp-python``` dependency included in this file. Make sure to update ```environment.yml``` to reflect the right flags for your platform (see available flags [here](https://github.com/abetlen/llama-cpp-python)).

For example, if you want it to run on CPU-only, the ```llama-cpp-python``` dependency in ```environment.yml``` will look like this:

```yml
name: local_llm_promptflow
...
dependencies:
...
 - pip:
    ...    
    - llama-cpp-python==0.2.56  # for CPU only
    ...
```

To run using the GPU on Mac:

```yml
name: local_llm_promptflow
...
dependencies:
...
 - pip:
    ...    
    - llama-cpp-python==0.2.56 -C cmake.args="-DLLAMA_METAL=on"  # for running on Mac GPU
    ...
```

After you have included the flags you want to use for ```llama-cpp-python```,  create the conda env by running:

```conda env create -f environment.yml```

## 2. Get a local model

LLM model files (in ```.gguf``` format) are stored in the ```models/``` directory. The Promptflow flow takes the model names as parameters. Without these, there is no LLM to run.

Model files in ```.gguf``` format can be downloaded from HuggingFace. Currently, I am experimenting with ```codellama-13b-instruct.Q5_K_M.gguf``` from [here](https://huggingface.co/TheBloke/CodeLlama-13B-Instruct-GGUF).

## 3. Install the Promptflow VS Code extension

Search for "Promptflow" in the VS Code extension catalogue and install it.

You can learn more about Promptflow from [the official docs](https://microsoft.github.io/promptflow/).

*Note: You can skip this step if you want to use Promptflow only from CLI/SDK, i.e. without the GUI provided by the VS Code plugin.*


# Running the flows

After going through the initial setup steps, you can start using the flows like so:
## ```local_codellama_flow```

You can start running the flow (see [the official Promptflow docs](https://microsoft.github.io/promptflow/)). Make sure to configure the flow inputs properly, according to your specific situation (e.g. ensure you point the flow to the right local model file).

It is NOT recommended to run batches with this flow, since loading the model at each inference is extremely inefficient.

## ```local_server_codellama_flow```

This flow involves a local server that the LLM sits in. The flow makes requests containing the user's inputs to this server in order to obtain responses from the LLM.
=======
If you have installed/changed any packages in the provided environment and wish to update it so that others can run your code, export the updated environment definition by running the command:


To use this flow:

1. Configure the LLM server

The server sits in the ```/llm_server``` directory. Within this directory, there is a ```server_config.yml``` file. Update this file to reflect your desired setup.

2. Start the server

 To start the server, run the following commands:

```cd llm_server/``` (assuming you start in the root of the repository)
 ```uvicorn server:app --host 127.0.0.1 --port 8000``` (or whatever host and port you want).

The server should now be running.

3. Use the Promptflow flow (as you normally would)

In case you have used another address/port for the server in the previous step, make sure to reflect this in the flow's inputs.

4. When you're done, kill the uvicorn server (```^C``` in the terminal).

# Other considerations

## For contributors

### Pre-commit hooks

Make sure the pre-commit hooks are installed before you start commiting to the repository. To do this, run ```pre-commit install``` in the root of the repo.

### Updating the conda environment


If you have installed/changed any packages in the provided environment, please update the ```environment.yml``` file **manually**. Exporting the file via ```conda export --from-history``` command seems to result in platform-dependent issues at times.
