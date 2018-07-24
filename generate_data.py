import numpy as np
import itertools
import matplotlib.pyplot as plt

def generate_true_values(num_trials, dt, x_init, y_init, a_x, a_y, x_y_only = False):
    """ Computes x, y, v_x, v_y assuming no acceleration and constant initial velocities of 0.
    Returns as a numpy array """
    x = np.zeros((4, num_trials))
    u = np.array([[a_x],
                  [a_y]])
    # initialize state vector
    init = np.array([x_init, y_init, 0, 0]) # assuming constant vel of 0
    init = init.reshape((-1,1))
    x[:, [0]] = init
    dt_sq = dt**2
    A = np.array([[1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [0, 0, 1, 0 ],
                  [0, 0, 0, 1 ]])
    B = np.array([[0.5*(dt_sq), 0],
                  [0, 0.5*(dt_sq)],
                  [dt, 0],
                  [0,dt]])
    time_int = dt*np.linspace(1, num_trials, num_trials)
    it = np.nditer(time_int, flags = ['c_index'])
    it.iternext() # continue past initial values
    while not it.finished:
        # constant accel, so there is no need for u to be a 2 by num_trials array; it can just be a 2 by 1 of the accel vals
        x[:, [it.index]] = np.dot(A,x[:, [it.index - 1]]) + np.dot(B,u)
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

def generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init, a_x, a_y):
    """ Simulates noisy sensor measurements with normally distributed noise estimates."""
    sensor_values = np.zeros((4,num_trials))
    x = generate_true_values(num_trials, dt, x_init, y_init, a_x, a_y, x_y_only=False)
    i = 0
    for i in range(0,num_trials):
        sensor_values[0,[i]] = np.random.normal(0,std_dev_x) + x[0,[i]]
        sensor_values[1,[i]] = np.random.normal(0,std_dev_y) + x[1,[i]]
        sensor_values[2,[i]] = np.random.normal(0,std_dev_y) + x[2,[i]]
        sensor_values[3,[i]] = np.random.normal(0,std_dev_y) + x[3,[i]]
        i += 1
    return sensor_values