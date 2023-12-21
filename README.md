## Getting Started
### Installation
You will need to have python downloaded or if running at LLNL on LC you will need to load the newest/newer version of python avalible on the host you are using.

``` bash
    module load python/3.9.12
```
Next we will create and enter a virtual enviornment.

``` bash
    python3 -m venv maestrowf_entk
    source maestrowf_entk/bin/activate
```

Update tools that we will be using to install the package.

``` bash
    pip install -U pip setuptools wheels
```

Install the package itself and then run a script that was installed to apply the plugin to our copy of maestro This does not change any default behavior of Maestrowf and there will be some output after running the `install-plugin` scipt saying that the patch has succeeded.

``` bash
    pip install git+https://github.com/MishaZakharchanka/maestrowf-entk
    install-plugin
```

### Running your first study
Now that the installation is complete you are ready to run your first study. If you have existing Maestrowf yaml files you can try to use one of those, otherwise there are a couple examples in the `input_examples` directory.

There are two different options you can use to launch the Radical entk backend when invoking Maestro:
`--entk` or `--entk_store_workflow`
The first will run your study and the latter will do the same but additionally output a JSON file with the information that is being passed from Meastro to Radical.

Running an example from the repository

``` bash
    maestro run --entk maestrowf-entk/input_examples/local_study.yaml
```