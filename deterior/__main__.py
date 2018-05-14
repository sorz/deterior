from argparse import ArgumentParser, FileType
from io import TextIOWrapper
import sys

from .dataset import DataSetReader, Record
from .trainning import build_simple_model, validate_model
from .models import Model


def _get_args():
    parser = ArgumentParser(
        description='Deterior - Equipment Deterioration Modeling Tools'
    )
    parser.add_argument(
        '-f', '--dataset-format',
        metavar='format.ini',
        dest='format',
        type=FileType('r', encoding='utf-8'),
        help='specify the format configuration for input dataset',
    )
    subparsers = parser.add_subparsers(
        title='tasks',
        dest='task',
        help='task that you want perform'
    )

    build = subparsers.add_parser(
        'build',
        help='build model from inspection records'
    )
    build.add_argument(
        'dataset',
        metavar='dataset.csv/.xlsx',
        type=FileType('rb'),
        help="a CSV file that contains inspection records"
    )
    build.add_argument(
        'model',
        metavar='output.json',
        type=FileType('w', encoding='utf-8'),
        help='where to save the model'
    )

    validate = subparsers.add_parser(
        'validate',
        help='validate a model by comparing its output with real '
             'inspection records'
    )
    validate.add_argument(
        'model',
        metavar='model.json',
        type=FileType(encoding='utf-8'),
        help='the model to verify'
    )
    validate.add_argument(
        'dataset',
        metavar='dataset.csv/.xlsx',
        type=FileType(encoding='utf-8'),
        help='a CSV file that contains inspection records'
    )

    args = parser.parse_args()
    if not args.task:
        parser.print_help()
        sys.exit(1)
    return args


def main():
    args = _get_args()
    if args.task == 'build':
        task_build(args)
    elif args.task == 'validate':
        task_validate(args)


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


def task_build(args):
    # TODO: add data format args
    records, n_state = _get_records(args)
    model, result = build_simple_model(n_state, records)
    # TODO: formating result
    print(result)
    if model:
        model.dump(args.model)
        print(f'Model saved as {args.model.name}')


def task_validate(args):
    # TODO: handle load error
    records, n_state = _get_records(args)
    model = Model.load(args.model)
    if n_state != model.n_state:
        print(f'Cannot verify {model.n_state}-state model on {n_state}-state '
              'dataset.', file=sys.stderr)
        sys.exit(1)
    validate_model(model, records)

if __name__ == '__main__':
    main()
