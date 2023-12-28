## Getting Started
### Installation
You will need to have python downloaded or if running at LLNL on LC you will need to load the newest/newer version of python avalible on the host you are using: (Note this is LC specific)

``` bash
    module load python/3.9.12
```
Next we will create and enter a virtual enviornment:

``` bash
    python3 -m venv {venv_name}
    source {venv_name}/bin/activate
```

Update tools that we will be using to install the package:

``` bash
    pip install -U pip setuptools wheel
```

Install the package itself and then run a script that was installed to apply the plugin to our copy of maestro This does not change any default behavior of Maestrowf and there will be some output after running the `install-plugin` scipt saying that the patch has succeeded.

``` bash
    pip install git+https://github.com/MishaZakharchanka/maestrowf-entk
    install-plugin
```

### Running your first study
Now that the installation is complete you are ready to run your first study. If you have existing Maestrowf yaml files you can try to use one of those, otherwise there are a couple examples in the `input_examples` directory (this directory is not installed so, the repository will need to be cloned to use it).

There are two different options you can use to launch the Radical entk backend when invoking Maestro:
`--entk` or `--entk_store_workflow`
The first will run your study and the latter will do the same but additionally output a JSON file with the information that is being passed from Meastro to Radical.

Running an example from the repository:

``` bash
    maestro run --entk maestrowf-entk/input_examples/local_study.yaml
```

## Additional Notes
### Idea behind eploring this integration
Radical's input or configuration file, which is used to tell Radical what jobs to run, has to be written in python. Maestrowf is also used to make scheduling many jobs with different parameters easier, but it uses yaml as the input. The hope was to be able to allow Radical users to create Maestro style yaml input that would then execute the jobs through Radical. Maybe yaml is easier to write and maintain, than python, for people who are not software engineers.

### Current status
As of now this plugin is not working, it gets hung up somewhere within Radical Saga. This was initially thought to be an issue with the shell that I was using while developing, zsh, but it seems that this issue persists even when using bash. The code was able to run locally at some point, but that stopped working so, it is possible that a bug was introduced in the plugin at some point when expanding the code to be able to run on remote hosts.

### Repository Contents
#### input_examples
This directory contains two very similar examples, that were built on Maestro's "Hello World" like example. One is run locally and does not launch batched jobs, the other is set up to run on Lassen, a host at LLNL, and will schedule the jobs to run on the working nodes.

#### llnl_resource_configs
This is a resource configuration file for Radical to be able to run on the Quartz host at LLNL. The file contained in this directory should be placed into `$HOME/.radical/pilot/configs/` so that Radical can find it. Additional hosts can be added to the dictionary, here is some Radical documentation that could help setting up more hosts:
* https://radicalpilot.readthedocs.io/en/devel/tutorials/configuration.html#User-defined-configuration
* https://radicalpilot.readthedocs.io/en/stable/tutorials/configuration.html#Customizing-a-predefined-configuration

#### src
This is the package directory that contains the script, `backend_entk.py`, which works as the interface between Maestro and Radical. There is also a patch file, `maestrowf_entk.patch`, for Maestro that is applied with the installed script, which is run at the end of the installation. Finally, `__init.py__` contains the script that is installed.

### Final thoughts
* `export RADICAL_LOG_LVL=DEBUG` is useful/nessesary for development, it will tell Radical to output logs you wouldn't see otherwise.
* We where trying to get the script that you have to run at the end of the `pip install` to be a part of the install, so that the user would only have to invoke one line and everything is set up. This seemed to work with a previous `setup.py` we were using, but once we updated pip it broke and I was unable to find a new way to do this.
* It might have been better to have this as a stand alone script, this would aleviate the install issues I mentioned above and could have been better for the longevity of the code as the patch file might have issues when Maestro is updated.