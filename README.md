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

## Usages

### Format of input dataset
Input inspection records is a table in either CSV (`.csv`) or MS Excel (`.xlsx`)
files. Table must contains a heading line as the first row of file. For Excel,
only the first Worksheet will be used.

The table must contains these 3 columns: `ID`, `State`, and `Time`. It may
contains other unrelated columns that will be ignored.

Each row in the table records one inspection action for one asset.
- `ID` is any string that can uniquely identify the asset being inspected.
- `Time` contains inspection date, default format is `YYYY-MM-DD`.
- `State` is a number or string represents the state of asset in this
  inspection.

The names of columns and format of date can be configured, see `footpath.ini`
for an example.

### Training

To training the models, use following command:
```bash
deterior build input.csv output.json
```

`input.csv` is the input dataset, the trained model will be saved as
`output.json` file, which can be used by this program with other tasks.

If you prefer to export internal _transition matrix_ of model to a CSV file,
`-t csv` argument can be used. For example,
```bash
deterior build input.csv -t csv output.csv
```

The outputted transition matrix is a table, where the number in *i*-row *j*-column
cell is the probability changing from state-*i* to state-*j*.

However, this is a export-only format, which cannot be use in this program again.

### Life curves

To plot life curve for a given model, use
```
deterior lifecurve --state 0 --from 0 --to 200 model.json
```
- `--state 0` specify the initial state in the beginning of simulation, default
  to `0`.
- `--from 0` specify the start time of the curve, default to `0`.
- `--to 0` specify the end time of the curve.
- `model.json` is the model to simulate. It is produced by `train` command of
  this program. 

This command will simulate deterioration process of the model, then pop up a
window showing the life curve. If you run it without a GUI environment,
`-w output.png` argument can be appended to get a image file instead of pop-up
window.

### Validation
You can use extra data as *test set* to validate the model trained before. Use
`validate` command for this, for example,
```
deterior validate model.json dataset.csv
```
- `model.json` is the trained model, produced by `deterior train` command.
- `dataset.csv` is the test data. Its format is the same as training.

It will output variance, error rate and other information.

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
