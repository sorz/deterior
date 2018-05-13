# deterior
Equipment Deterioration Modeling Tools

## Install

### Prerequisites

- Python (>= 3.6)
  
- Python `pip` tool

For Windows, download the lastest version of Python from
[python.org](https://python.org), `pip` tool is included by default.

For Linux, most distros have Python installed by default, but please
confirm its version (must be 3.6 or newer).
Common package name for `pip` is `python3-pip` or just `python-pip`.

### Install from source code
Change current working directory to where `setup.py` file locates,
then run:
```
pip3 install --user .
```
It will build and install _deterior_ with its dependences.

Now you can run `deterior` to confirm the installation:
```
deterior --help
```
If the system cannot find `deterior`, you can also use:
```
python3 -m deterior --help
```
