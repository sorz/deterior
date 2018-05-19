from collections import defaultdict
import sys
import numpy as np
from scipy import optimize

from .models import SimpleModel, Model, TimeStates
from .dataset import Record


def _prepare_validate(n_state: int, records: [Record]) \
        -> (TimeStates, np.ndarray):
    """Return (time_states, final_states)."""
    time_states = defaultdict(lambda: np.zeros([n_state]))
    final_states = np.zeros([n_state])
    for s0, s1, t in records:
        time_states[t][s0] += 1
        final_states[s1] += 1
    return time_states, final_states

def build_simple_model(n_state: int, records: [Record]):
    time_states, final_states = _prepare_validate(n_state, records)
    def loss(param):
        model = SimpleModel(param)
        expect = model.simulate(time_states)
        diff = final_states - expect
        return np.sum(diff ** 2)

    n_params = n_state - 1
    init = np.array([0.1] * n_params)
    bounds = [(0, 1)] * n_params
    result = optimize.minimize(loss, init, bounds=bounds)
    if result.fun > 1:
        print(f'Loss {result.fun} too large, '
              'use differential evolution', file=sys.stderr)
        result = optimize.differential_evolution(loss, bounds)
    if not result.success:
        return None, result
    return SimpleModel(result.x), result


def validate_model(model: Model, records: [Record]):
    time_states, final_states = _prepare_validate(model.n_state, records)
    expect = model.simulate(time_states)
    diff = final_states - expect
    var = np.sum(diff ** 2)
    std = np.sqrt(var)
    err = std / np.sum(expect) * 100
    np.set_printoptions(precision=2)
    print(f"Exception: {expect}")
    print(f"Actual:    {final_states}")
    print(f"Variance:  {var:.3f}")
    print(f"StdDev:    {std:.3f}")
    print(f"Error:     {err:.3f}%")
