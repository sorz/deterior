from argparse import ArgumentParser, FileType, Namespace
import sys

from . import tasks


def _get_args() -> Namespace:
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

    model = dict(
        metavar='model.json',
        type=FileType(encoding='utf-8'),
        help="the input model"
    )
    dataset = dict(
        metavar='dataset.csv',
        type=FileType('rb'),
        help='a comma-separated values (.csv) or Microsoft Excel (.xlsx) file '
             'that contains inspection records'
    )

    build = subparsers.add_parser(
        'build',
        help='build model from inspection records'
    )
    build.add_argument('dataset', **dataset)
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
    validate.add_argument('model', **model)
    validate.add_argument('dataset', **dataset)

    lifecurve = subparsers.add_parser(
        'lifecurve',
        help='plot life curve for a given model',
    )
    lifecurve.add_argument('model', **model)
    lifecurve.add_argument(
        '-s', '--state',
        metavar='N', type=int, default=0,
        help='initial state, default to the first state "0"',
    )
    lifecurve.add_argument(
        '--from',
        metavar='T0', dest='start', type=int, default=0,
        help='start time of the simulation',
    )
    lifecurve.add_argument(
        '--to',
        metavar='T1', dest='stop', type=int, required=True,
        help='end time of the simulation',
    )
    lifecurve.add_argument(
        '--step',
        metavar='S', type=int, default=0,
        help='time step, the time interval between two simulations'
    )
    lifecurve.add_argument(
        '-w', '--save-to',
        dest='output',
        metavar='figure.png',
        type=FileType('wb'),
        help='save figure as image file instead of showing on pop-up window'
    )

    args = parser.parse_args()
    if not args.task:
        parser.print_help()
        sys.exit(1)
    return args


def main() -> None:
    args = _get_args()
    task = getattr(tasks, args.task)
    task(args)

if __name__ == '__main__':
    main()
