import numpy as np
import generate_data
import matplotlib.pyplot as plt

def kalman_filter(num_trials, x_init, y_init):
    dt = 0.001
    # std_dev_x and std_dev_y of sensors is 3m
    # generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init)
    noisy_readings = generate_data.generate_noisy_values(num_trials, dt, 2, 2, x_init,y_init)

    A = np.array([[1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0 ],
                [0, 0, 0, 1 ]])

    H = np.eye(4)

    # Init var of x and y are large because uncertain of original position.
    # Init var of vel_x and vel_y are 0.1.
    # There are no covariances as each state var is independent.

    P = np.array([ [500, 0, 0, 0],
                    [0, 500, 0, 0],
                    [0, 0, 0.1, 0],
                    [0, 0, 0, 0.1]])
    
    Q = np.zeros(4) # assuming no process noise

    R = np.array([ [9, 0, 0, 0],
                    [0, 9, 0, 0],
                    [0, 0, 0.01, 0],
                    [0, 0, 0, 0.01]])
    
    state = np.zeros((4, num_trials))
    # init state
    state[:, [0]] = np.array([[0, 0, x_init, y_init]]).T

    for i in range(1, num_trials):
        state[:,[i]] = np.dot(A,state[:, [i - 1]]) + 0 # 0 is for w
        P = np.dot(np.dot(A,P),A.T) + Q

        # gain
        K_num = np.dot(P, H.T)
        K_denom = np.dot(np.dot(H,P),H.T) + R

    # TODO: K is current a 4x4 matrix, which will pose problems in the update step as the sensor simulation comes in as a 2x1 instead of a 4x1
    # To remedy, change the sensor measurements to be 4x1 (include v_x and v_y). This can be done with x_y_only.
    # Plot everything after this