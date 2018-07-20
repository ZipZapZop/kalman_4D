import numpy as np
import generate_data
import matplotlib.pyplot as plt

def kalman_filter(num_trials, x_init, y_init):
    dt = 0.001
    # std_dev_x and std_dev_y of sensors is 3m
    # generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init)
    noisy_readings = generate_data.generate_noisy_values(num_trials, dt, 2, 2, x_init,y_init)   # 4xnum_trials

    A = np.array([[1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0 ],
                [0, 0, 0, 1 ]])

    H = np.eye(4)

    # Init var of x and y are large because uncertain of original position.
    # Init var of vel_x and vel_y are 0.1.
    # All covariances are equal to 0 as each state var is assumed independent.

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
        K = np.dot(K_num,np.linalg.inv(K_denom))

        innovation = noisy_readings[:,[i]] - np.dot(H,state[:,[i-1]])
        state[:,[i]] = state[:,[i]]+ np.vstack(np.dot(K,innovation))
        P = np.dot(np.eye(4) - np.dot(K,H),P)

    return state

x = kalman_filter(10,2,2)
print(np.shape(x))
print(x)

def plot_kalman(num_trials, x_init, y_init):
    fig = plt.figure()
    states = kalman_filter(num_trials, x_init, y_init) # 4 x num_trials
    estimates = generate_data.generate_true_values(num_trials,0.001,x_init,y_init,x_y_only=False)

    ax1 = fig.add_subplot(211)  # x values
    plt.plot(states[0],label = 'Predicted values')
    plt.plot(estimates[0],label = 'Estimated values')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.set_title('x position')

    ax2 = fig.add_subplot(212)  # y values
    plt.plot(states[1])
    plt.plot(estimates[1])
    # handles and labels for ax2 are same as those for ax1
    ax2.set_title('y position')

    fig.legend(handles, labels)
    fig.subplots_adjust(hspace=.5)


    plt.show()

plot_kalman(1000,2,2)
