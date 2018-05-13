from argparse import ArgumentParser, FileType
import sys

from .dataset import load_inspect_log
from .trainning import build_simple_model, validate_model
from .models import Model


def _get_args():
    parser = ArgumentParser(
        description='Equipment Deterioration Modeling Tool'
    )
    subparsers = parser.add_subparsers(
        title='tasks',
        dest='task',
        help='Task that you want perform'
    )

    build = subparsers.add_parser(
        'build',
        help='Build model from inspection records'
    )
    build.add_argument(
        'dataset',
        metavar='dataset.csv',
        type=FileType(encoding='utf-8'),
        help="A CSV file that contains inspection records"
    )
    build.add_argument(
        'model',
        metavar='output.json',
        type=FileType('w', encoding='utf-8'),
        help='Where to save the model'
    )

    validate = subparsers.add_parser(
        'validate',
        help='Validate a model by comparing its output with real '
             'inspection records'
    )
    validate.add_argument(
        'model',
        metavar='model.json',
        type=FileType(encoding='utf-8'),
        help='The model to verify'
    )
    validate.add_argument(
        'dataset',
        metavar='dataset.csv',
        type=FileType(encoding='utf-8'),
        help='A CSV file that contains inspection records'
    )

    return parser.parse_args()


def main():
    args = _get_args()
    if args.task == 'build':
        task_build(args)
    elif args.task == 'validate':
        task_validate(args)


def task_build(args):
    # TODO: add data format args
    records, n_state = load_inspect_log(args.dataset)
    model, result = build_simple_model(n_state, records)
    # TODO: formating result
    print(result)
    if model:
        model.dump(args.model)
        print(f'Model saved as {args.model.name}')


def task_validate(args):
    # TODO: handle load error
    model = Model.load(args.model)
    records, n_state = load_inspect_log(args.dataset)
    if n_state != model.n_state:
        print(f'Cannot verify {model.n_state}-state model on {n_state}-state '
              'dataset.', file=sys.stderr)
        sys.exit(1)
    validate_model(model, records)

if __name__ == '__main__':
    main()
