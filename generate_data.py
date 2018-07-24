import numpy as np
import itertools
import matplotlib.pyplot as plt

def generate_true_values(num_trials, dt, x_init, y_init, x_y_only = False):
    """ Computes x, y, v_x, v_y assuming no acceleration and constant initial velocities of 2.
    Returns as a numpy array """
    x = np.zeros((4, num_trials))

    # initialize state vector
    init = np.array([x_init, y_init, 2, 2]) # assuming constant vel of 2
    init = init.reshape((-1,1))
    x[:, [0]] = init
    A = np.array([[1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [0, 0, 1, 0 ],
                  [0, 0, 0, 1 ]])

    time_int = dt*np.linspace(1, num_trials, num_trials)
    it = np.nditer(time_int, flags = ['c_index'])
    it.iternext() # continue past initial values
    while not it.finished:
        x[:, [it.index]] = np.dot(A,x[:, [it.index - 1]])
        it.iternext()
    
    it.reset()

    if not x_y_only:
         return x
    
    pos_only = np.zeros((2, num_trials))
    while not it.finished:
        pos_only[0, it.index] = x[0, it.index]
        pos_only[1, it.index] = x[1, it.index]
        it.iternext()

    return pos_only

def generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init):
    """ Simulates noisy sensor measurements with normally distributed noise estimates."""
    sensor_values = np.zeros((4,num_trials))
    x = generate_true_values(num_trials, dt, x_init, y_init, x_y_only=False)
    i = 0
    for i in range(0,num_trials):
        sensor_values[0,[i]] = np.random.normal(0,std_dev_x) + x[0,[i]]
        sensor_values[1,[i]] = np.random.normal(0,std_dev_y) + x[1,[i]]
        sensor_values[2,[i]] = np.random.normal(0,std_dev_y) + x[2,[i]]
        sensor_values[3,[i]] = np.random.normal(0,std_dev_y) + x[3,[i]]
        i += 1
    return sensor_values
