from collections import defaultdict
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
    init = np.array([0.5] * n_params)
    bounds = [(0, 1)] * n_params
    result = optimize.minimize(loss, init, bounds=bounds)
    if result.success:
        return SimpleModel(result.x), result
    else:
        return None, result


def validate_model(model: Model, records: [Record]):
    time_states, final_states = _prepare_validate(model.n_state, records)
    expect = model.simulate(time_states)
    variance = np.sum((final_states - expect) ** 2)
    print(f"Expection: {expect}")
    print(f"Actual:    {final_states}")
    print(f"Variance:  {variance}")
