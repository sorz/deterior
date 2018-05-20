from io import TextIOWrapper
from argparse import Namespace
import sys
import matplotlib.pyplot as plt

from .models import Model
from .dataset import DataSetReader, Record
from .trainning import build_simple_model
from .evaluation import validate_model, corss_validate


def _get_records(args) -> ([Record], int):
    reader = DataSetReader(args.format)
    if args.dataset.name.endswith('.csv'):
        csvfile = TextIOWrapper(args.dataset, 'utf-8')
        records, n_state = reader.load_csv(csvfile)
    elif args.dataset.name.endswith('.xlsx'):
        records, n_state = reader.load_xls(args.dataset)
    else:
        print(f'Unknown file type: {args.dataset.name}, '
              'please rename its suffix to either .csv or .xlsx.',
              file=sys.stderr)
        sys.exit(1)
    print(f'{len(records)} inspection records loaded')
    return records, n_state


def build(args: Namespace) -> None:
    """Build task. Tranining model with records and save the model.
    """
    records, n_state = _get_records(args)
    print('Training...')
    model, result = build_simple_model(n_state, records)
    if model:
        print('Done')
        print(f'  Iterations: {result.nit}')
        print(f'        Loss: {result.fun}')
        print(f'  Parameters: {result.x}')
        model.dump(args.model)
        print(f'Model saved as {args.model.name}')
    else:
        print('Failed:', result.message)
        print(result)


def cross(args: Namespace) -> None:
    """Corss task. Corss validate model on given dataset."""
    records, n_state = _get_records(args)
    result = corss_validate(n_state, records, args.k)
    print(f"Mean Variance: {result.var:.3f}")
    print(f"Mean StdDev:   {result.std:.3f}")
    print(f"Mean Error:    {result.err:.3f}%")


def validate(args: Namespace) -> None:
    """Validate task. Compare output of given model and dataset.
    """
    # TODO: handle load error
    records, n_state = _get_records(args)
    model = Model.load(args.model)
    if n_state != model.n_state:
        print(f'Cannot verify {model.n_state}-state model on {n_state}-state '
              'dataset.', file=sys.stderr)
        sys.exit(1)
    result = validate_model(model, records)
    print(f"Exception: {result.expect}")
    print(f"Actual:    {result.actual}")
    print(f"Variance:  {result.var:.3f}")
    print(f"StdDev:    {result.std:.3f}")
    print(f"Error:     {result.err:.3f}%")


def lifecurve(args: Namespace) -> None:
    """Lifecurve task. Plot the life curve for given model.
    """
    model = Model.load(args.model)
    curve = model.simulate_curve(
        args.state, args.start, args.stop, args.step
    )
    plt.title('Life curve')
    plt.xlabel('Time')
    plt.ylabel('Probability')
    plt.grid(True)
    xs = list(range(args.start, args.stop, args.step))
    for i in range(args.state, model.n_state):
        plt.plot(xs, curve[:,i], label=f'State {i}')
    plt.legend()
    if args.output:
        plt.savefig(args.output)
        print(f'Figure saved as {args.output.name}')
    else:
        plt.show()
