from itertools import chain
from collections import namedtuple
import sys
import numpy as np

from .models import Model
from .dataset import Record
from .training import prepare_validate, build_simple_model


Result = namedtuple('Reulst', ['expect', 'actual', 'var', 'std', 'err'])

def validate_model(model: Model, records: [Record]) -> Result:
    time_states, final_states = prepare_validate(model.n_state, records)
    expect = model.simulate(time_states)
    diff = final_states - expect
    var = np.sum(diff ** 2)
    std = np.sqrt(var)
    err = std / np.sum(expect) * 100
    np.set_printoptions(precision=2)
    return Result(expect, final_states, var, std, err)


def _split(l, k) -> [[Record]]:
    """Split list `l` to `k` lists."""
    n =  int(np.ceil(len(l) / k))
    for i in range(0, len(l), n):
        yield l[i:i + n]


def corss_validate(n_state: int, records: [Record], k: int) -> Result:
    np.random.shuffle(records)
    folds = list(_split(records, k))
    k = len(folds)
    print('Size of each sub-sample:', len(folds[0]))
    var, std, err = [], [], []
    for i in range(k):
        print(f'Test on fold {i + 1}...')
        test = folds[i]
        train = chain(*folds[:i], *folds[i:])
        model, result = build_simple_model(n_state, train)
        if model is None:
            print(f'Fail to build model: {result.message}', file=sys.stderr)
            return
        result = validate_model(model, test)
        var.append(result.var)
        std.append(result.std)
        err.append(result.err)
    var = np.sum(var) / k
    std = np.sum(std) / k
    err = np.sum(err) / k
    return Result(None, None, var, std, err)
