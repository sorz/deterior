# Deterior
A Markov chain-based infrastructure asset deterioration modelling tools.

This is one part of outcome in the course _COMP90055 Computing Project_.

## Install

### Prerequisites

- Python (>= 3.6)
  
- Python `pip` tool

For Windows, download the latest version of Python from
[python.org](https://www.python.org/downloads/),
the `pip` tool is included by default.

For Linux, most distros have Python installed by default, but please confirm its
version (must be 3.6 or newer). Common package name for `pip` is `python3-pip`
or just `python-pip`.

### Install from source code
Just run:
```
pip3 install --user git+https://github.com/sorz/deterior
```
It will build and install _deterior_ with its dependences.

Now you can run `deterior` to confirm the installation:
```
deterior --help
```
If the system cannot find `deterior` command, you can also use:
```
python3 -m deterior --help
```

## Acknowledgements

This software uses following libraries:

- [NumPy](https://www.numpy.org/)
- [SciPy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)

## License
This software is licensed under

- CC BY 4.0 International 
- MIT License

This code is allowed to be adapted, shared and allowed for commercial uses.
