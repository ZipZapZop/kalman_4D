import numpy as np
import generate_data
import matplotlib.pyplot as plt

def kalman_filter(num_trials, x_init, y_init, a_x, a_y):
    """ kalman_filter() applies a Kalman filter on the simulated noisy output from generate_data.py. 
    The velocity is held constant at 2 m/s. This value can be changed in the generate_values.py source. 
    There is assumed to be no noise in the prediction step of the filter and hence, the process noise covariance matrix
    and the predicted state noise matrix are set to zero matrices.
    Measurements are taken at every 0.001 second (dt). This can be changed in the kalman.py source.
    """

    dt = 0.001
    dt_sq = dt**2
    # std_dev_x and std_dev_y of sensors is 3m
    # generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init)
    noisy_readings = generate_data.generate_noisy_values(num_trials, dt, 20, 20, x_init,y_init, a_x, a_y)   

    A = np.array([[1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0 ],
                [0, 0, 0, 1 ]])

    B = np.array([[0.5*(dt_sq), 0],
                  [0, 0.5*(dt_sq)],
                  [dt, 0],
                  [0,dt]])
    H = np.eye(4)

    # Init var of x and y are large because uncertain of original position.
    # Vel_x and vel_y are 0.1.
    # All covariances are equal to 0 as each state var is assumed independent.

    P = np.array([ [500, 0, 0, 0],
                    [0, 500, 0, 0],
                    [0, 0, 0.1, 0],
                    [0, 0, 0, 0.1]])
    
    variances = np.zeros((4,num_trials))

    Q = np.zeros(4) # assuming no process noise

    R = np.array([ [9, 0, 0, 0],
                    [0, 9, 0, 0],
                    [0, 0, 0.01, 0],
                    [0, 0, 0, 0.01]])
    
    state = np.zeros((4, num_trials))
    
    # initialize state
    state[:, [0]] = np.array([[0, 0, x_init, y_init]]).T

    u = np.array([[a_x],
                  [a_y]])

    for i in range(1, num_trials):
        state[:,[i]] = np.dot(A,state[:, [i - 1]]) +  np.dot(B,u) + np.zeros((4,1)) # the predicted state noise is set to 0
        P = np.dot(np.dot(A,P),A.T) + Q

        # gain
        K_num = np.dot(P, H.T)
        K_denom = np.dot(np.dot(H,P),H.T) + R
        K = np.dot(K_num,np.linalg.inv(K_denom))

        # Update
        innovation = noisy_readings[:,[i]] - np.dot(H,state[:,[i-1]])
        state[:,[i]] = state[:,[i]]+ np.vstack(np.dot(K,innovation))
        P = np.dot(np.eye(4) - np.dot(K,H),P) + np.zeros((4,4))

        # save variances at each step
        varianceToSave = np.array([[P[0,0]],
                           [P[1,1]],
                           [P[2,2]],
                           [P[3,3]]])
        variances[:,[i]] = varianceToSave

        
    return state, variances

def plot_states(num_trials, x_init, y_init, a_x, a_y):
    """ Calls kalman_filter() and plots the prediction and correction at every time interval
    for both position and velocity. In another figure, plots the variances of each state 
    variable over time. The initial covariances are 0 in this model, and therefore are 
    not plotted."""

    states, variances = kalman_filter(num_trials, x_init, y_init, a_x, a_y)
    
    fig = plt.figure(num=1,figsize=(12, 10), dpi=100)
    estimates = generate_data.generate_true_values(num_trials,0.001,x_init,y_init, a_x, a_y)

    ax1 = fig.add_subplot(221)  # x values
    plt.plot(states[0],label = 'Predicted values')
    plt.plot(estimates[0],label = 'Estimated values')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.set_title('x position')

    ax2 = fig.add_subplot(222)  # y values
    plt.plot(states[1])
    plt.plot(estimates[1])
    ax2.set_title('y position')

    ax3 = fig.add_subplot(223) # v_x values
    plt.plot(states[2])
    plt.plot(estimates[2])
    ax3.set_title('$v_x$ values')

    ax4 = fig.add_subplot(224) # v_y values
    plt.plot(states[3])
    plt.plot(estimates[3])
    ax4.set_title('$v_y$ values')

    fig.legend(handles, labels)     # handles and labels for ax2, ax3, ax4 are same as for ax1
    fig.subplots_adjust(hspace=.2,wspace=.2)
    
    plt.show()


def plot_variances(num_trials, x_init, y_init, a_x, a_y):
    states, variances = kalman_filter(num_trials, x_init, y_init, a_x, a_y)

    fig2 = plt.figure(num=2,figsize=(12,10),dpi=100)

    bx1 = fig2.add_subplot(221)
    plt.plot(variances[0])
    plt.yscale('log')
    bx1.set_title('${\sigma_x}^2$')
    
    bx2 = fig2.add_subplot(222, sharex=bx1)
    plt.plot(variances[1])
    plt.yscale('log')
    bx2.set_title('${\sigma_y}^2$')

    bx3 = fig2.add_subplot(223, sharex=bx1)
    plt.plot(variances[2])
    plt.yscale('log')
    bx3.set_title('${\sigma_{v_x}}^2$')

    bx4 = fig2.add_subplot(224, sharex=bx1)
    plt.plot(variances[3])
    plt.yscale('log')
    bx4.set_title('${\sigma_{v_y}}^2$')

    plt.show()


# num_trials=1000, x_init=2, y_init=2, a_x = a_y = 0.1
plot_variances(1000,2,2, 2, 2)
