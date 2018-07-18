import numpy as np
import matplotlib.pyplot as plt
import itertools

''' Computes x, y, v_x, v_y assuming no acceleration and constant initial velocities of 1.
    Returns as a numpy array '''
    
def generate_true_values(num_estimates, dt, x_init, y_init, x_y_only = 'False'):
    x = np.zeros((4, num_estimates))

    # init state vector
    x[:,[0]] = np.array([x_init, y_init, 1, 1]).T
    A = np.array( [1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [0, 0, 1, 0 ],
                  [0, 0, 0, 1 ])

    time_int = dt*np.linspace(1, num_estimates, num_estimates)
    it = np.nditer(time_int, flags = ['c_index'])
    it.iternext() # continue past init values
    while not it.finished:
        x[:,[it.index]] = np.dot(A,x[:,[it.index - 1]])
        it.iternext()
    
    it.reset()

    if not x_y_only:
         return x
    
    pos_only = np.zeros((2, num_estimates))
    while not it.finished:
        pos_only[0, it.index] = x[0, it.index]
        pos_only[1, it.index] = x[1, it.index]
        it.iternext()

    return pos_only