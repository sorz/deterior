import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, TextIO
import numpy as np

from . import __version__ as version


TimeStates =  Dict[int, np.ndarray]

class Model:
    def __init__(self, prob_matrix: np.matrix) -> None:
        """Build a model by given probability matrix.
        """
        self.mat = prob_matrix
        self.n_state = prob_matrix.shape[0]
        if prob_matrix.shape != (self.n_state, self.n_state):
            raise ValueError('shape of probability matrix must be (n x n)')
        for i in range(self.n_state):
            if not 0.999999 < np.sum(self.mat[i]) < 1.000001:
                raise ValueError(f'sum of row {i} in probability matrix != 1')

    def simulate(self, time_states: TimeStates) -> np.ndarray:
        """Given times and initial state vectors, return expectation of final
        states.
        """
        exp = np.mat(np.zeros(self.n_state))
        for time, states in time_states.items():
            exp += states * self.mat ** time
        return np.array(exp)[0]

    def simulate_curve(self,
                       init_state: int,
                       start: int, stop: int, step: int) -> np.ndarray:
        mat = self.mat ** start
        init = np.zeros(self.n_state)
        init[init_state] = 1
        rows = len(range(start, stop, step))
        exps = np.zeros([rows, self.n_state])
        for i in range(rows):
            exps[i] = init * mat
            mat *= self.mat ** step
        return exps

    def dump(self, fp: TextIO) -> None:
        """Dump the model into file-like object `fp`"""
        mat = defaultdict(dict)
        for i in range(self.n_state):
            for j in range(self.n_state):
                if self.mat[i, j] > 0:
                    mat[i][j] = self.mat[i, j]
        obj = {
            '_note': f'Model dumped by Deterior v{version}',
            '_saved_at': datetime.now().isoformat(),
            'type': f'{type(self).__name__}',
            'n_state': self.n_state,
            'transition_matrix': mat,
        }
        json.dump(obj, fp, indent=2)

    @staticmethod
    def load(fp: TextIO):
        """Load the model from file-like object `fp`"""
        obj = json.load(fp)
        n = obj['n_state']
        mat = np.mat(np.zeros([n, n]))
        for i, cols in obj['transition_matrix'].items():
            for j, p in cols.items():
                mat[int(i), int(j)] = p
        return Model(mat)


class SimpleModel(Model):

    def __init__(self, probs) -> None:
        """Build a n-state model by given parameters.

        `probs` is a list of probability of changing to the next state.
        Its length is total states of this model minus one.
        """
        if not all(0 <= p <= 1.000001 for p in probs):
            raise ValueError('each p in probs must between 0 and 1')

        n = len(probs) + 1
        mat = np.mat(np.zeros([n, n]))
        mat[n-1, n-1] = 1
        for i in range(n-1):
            mat[i, i] = 1 - probs[i]
            mat[i, i+1] = probs[i]
        super().__init__(mat)
