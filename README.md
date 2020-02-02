# Monopoly Simulator
A simulator for a simplified version of the monopoly game


## Install Guide

*This project is meant to run using **python 3.7** or greater, other versions may not work.*

As usual its strongly recommended to run service in a virtual environment.
``
### Clone project
```sh
$ git@github.com:hbontempo-br/monopoly-simulator.git
```

### Setup a Virtual Environmnet
For linux/Debian distros:
```sh
$ sudo apt-get python3-venv
$ python3 -m venv .venv
$ source .venv/bin/activate
```


## Usage

Just run the simulation [script](simulation.py) `simulation.py`.

```sh
$ python3 simulation.py
```

To alter the default behaviour please check the `constants.py` [file](constants.py) . 
This file centralizes all constants used in the project.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

This project has a strict formatting validation, but it's super easy to adhere to. Just use the automatic pre-commit.

### Install the pre commit:

From inside the project's folder:

```sh
$ pip3 install -r requirements-dev.txt
$ pre-commit install
```

### Using it:

Just make a commit! On every commit now on all the super strict formatting is taken care of automagically.

If you want to run the validation without a commit just run:
```sh
$ pre-commit run --all-files
```

## Tests

```
NOT IMPLEMENTED
```


<br/>
<br/>
<br/>

---

#### TODOs:
- Design tests.
