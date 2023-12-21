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

Install the package itself and then run a script that was installed to apply the plugin to our copy of maestro. (This does not change any default behavior of maestrowf). You should see some output after running the `install-plugin` scipt saying that the patch has succeeded.

``` bash
    pip install git+https://github.com/MishaZakharchanka/maestrowf-entk
    install-plugin
```
