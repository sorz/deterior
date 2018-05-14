from io import TextIOWrapper
from argparse import Namespace
import sys
import matplotlib.pyplot as plt

from .models import Model
from .dataset import DataSetReader, Record
from .trainning import build_simple_model, validate_model


def _get_records(args) -> ([Record], int):
    reader = DataSetReader(args.format)
    if args.dataset.name.endswith('.csv'):
        csvfile = TextIOWrapper(args.dataset, 'utf-8')
        return reader.load_csv(csvfile)
    elif args.dataset.name.endswith('.xlsx'):
        return reader.load_xls(args.dataset)

    print(f'Unknown file type: {args.dataset.name}, '
          'please rename its suffix to either .csv or .xlsx.',
          file=sys.stderr)
    sys.exit(1)


def build(args: Namespace) -> None:
    records, n_state = _get_records(args)
    model, result = build_simple_model(n_state, records)
    # TODO: formating result
    print(result)
    if model:
        model.dump(args.model)
        print(f'Model saved as {args.model.name}')


def validate(args: Namespace) -> None:
    # TODO: handle load error
    records, n_state = _get_records(args)
    model = Model.load(args.model)
    if n_state != model.n_state:
        print(f'Cannot verify {model.n_state}-state model on {n_state}-state '
              'dataset.', file=sys.stderr)
        sys.exit(1)
    validate_model(model, records)


def lifecurve(args: Namespace) -> None:
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
