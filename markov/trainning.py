from collections import defaultdict
import numpy as np
from scipy import optimize

from .models import SimpleModel
from .dataset import Record


def build_simple_model(n_state: int, records: [Record]):
    time_states = defaultdict(lambda: np.zeros([n_state]))
    final_states = np.zeros([n_state])
    for s0, s1, t in records:
        time_states[t][s0] += 1
        final_states[s1] += 1

    def loss(param):
        model = SimpleModel(param)
        exp = np.mat(np.zeros(n_state))
        for time, states in time_states.items():
            exp += states * model.mat ** time
        diff = final_states - np.array(exp)[0]
        return np.sum(diff ** 2)

    n_params = n_state - 1
    init = np.array([0.5] * n_params)
    bounds = [(0, 1)] * n_params
    result = optimize.minimize(loss, init, bounds=bounds)
    if result.success:
        return SimpleModel(result.x), result
    else:
        return None, result
