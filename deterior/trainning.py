import sys
from collections import defaultdict
from scipy import optimize
import numpy as np

from .models import SimpleModel, TimeStates
from .dataset import Record


def prepare_validate(n_state: int, records: [Record]) \
        -> (TimeStates, np.ndarray):
    """Convert records to (time_states, final_states)."""
    time_states = defaultdict(lambda: np.zeros([n_state]))
    final_states = np.zeros([n_state])
    for s0, s1, t in records:
        time_states[t][s0] += 1
        final_states[s1] += 1
    return time_states, final_states


def build_simple_model(n_state: int, records: [Record]):
    time_states, final_states = prepare_validate(n_state, records)
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
