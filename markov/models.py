import numpy as np


class Model:
    def __init__(self, prob_matrix):
        """Build a model by given probability matrix.
        """
        self.mat = prob_matrix
        self.n_state = prob_matrix.shape[0]        
        if prob_matrix.shape != (self.n_state, self.n_state):
            raise ValueError('shape of probability matrix must be (n x n)')

    def simulate(self, states, time):
        return states * self.mat ** time


class SimpleModel(Model):

    def __init__(self, probs):
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
