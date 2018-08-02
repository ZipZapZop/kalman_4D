import kalman
import generate_data
import numpy as np
import matplotlib.pyplot as plt


def calculate_differences(num_trials, x_init, y_init, a_x, a_y, dt):
    """ Simply subtracts values calculated from a kalman filter and theoretical values. This tells us how impactful the kalman filter was at a certain point in time. The
    difference is calculated in the x as well as the y dimension. """
    filtered, _ = kalman.kalman_filter(num_trials,x_init,y_init,a_x,a_y) # returns x, y, and v_x, v_y
    true_vals = generate_data.generate_true_values(num_trials, dt, x_init,y_init, a_x, a_y, x_y_only=True)

    differences = np.zeros((2,num_trials))

    for i in range(0,num_trials):
        diff_x = true_vals[0,i] - filtered[0,i]
        differences[0,i] = diff_x

        diff_y = true_vals[1,i] - filtered[1,i]
        differences[1,i] = diff_y

    return differences


def plot_differences(num_trials, x_init, y_init, a_x, a_y, dt):
    """ Plots a graph displaying the differences calculated in calculate_differences. """
    x = calculate_differences(num_trials, x_init, y_init, a_x , y_init, dt)

    plt.figure()
    plt.plot(x[0], label='Difference in x')
    plt.plot(x[1], label='Difference in y')
    plt.legend()
    plt.show()

# plot_differences(10000,0,0,0.1,0.1,0.001)

def MSE(num_trials, x_init, y_init, a_x, a_y, dt, q):
    """ Calculates the mean squared error at each time interval. The filter is run q times and an error value is calculated with these values. """
    all_trial_data = np.zeros((2, num_trials, q))
    for i in range(0,q):
        all_trial_data[:,:,i] = calculate_differences(num_trials, x_init, y_init, a_x, a_y, dt)
    
    summed_error = np.zeros((2, num_trials))

    for i in range(0,num_trials):
        all_trial_data[:,i,:] = all_trial_data[:,i,:]**2
        trial_sum_x = all_trial_data[0,i,:].sum()
        trial_sum_y = all_trial_data[1,i,:].sum()
        MSE_x = trial_sum_x/q
        MSE_y = trial_sum_y/q
        summed_error[0,i] = MSE_x
        summed_error[1,i] = MSE_y

    return summed_error

def mean_squared_error(num_trials, x_init, y_init, a_x, a_y, dt, q):
    """ Calculates the mean squared error at each time interval. The filter is run
    q times and an error value is calculated with these values. """

    # 3D array that stores in each index the sum of all errors from all previous indices

    all_diff = np.zeros((2, num_trials, q))

    # Run KF and therefore error calculator for q trials.
    # The more trials, the more accurate.
    # Calculate all the differences for the qth trial, square each one, and store
    # each in an array for later use.
    for i in range(0, q):
        differences = calculate_differences(num_trials, x_init, y_init, a_x, a_y, dt)

        # Squares each difference value and adds it to all previous difference values.
        # Stores the new value in the nth time interval

        # initial values
        all_diff[0,0,0] = differences[0,0]
        all_diff[1,0,0] = differences[1,0]
        for j in range(1, num_trials):
            all_diff[0, j, i] = all_diff[0, j - 1, i] + differences[0, j]**2
            all_diff[1, j, i] = all_diff[1, j - 1, i] + differences[1, j]**2

    MSE = np.zeros((2,num_trials))

    for i in range(0, num_trials):
        sum_x = 0
        sum_y = 0
        # horrible cache-wise because reading in column-order
        # TODO: rearrange all_diff array so that calculations are in column order?
        for j in range(0,q):
            sum_x = sum_x + all_diff[0, i, j]
            sum_y = sum_y + all_diff[1, i, j]
        
        MSE[0, i] = sum_x/num_trials
        MSE[1, i] = sum_y/num_trials

    return MSE

def plot_MSE(num_trials, x_init, y_init, a_x, a_y, dt, q):
    x = MSE(num_trials, x_init, y_init, a_x, a_y, dt, q)
    print(x)
    print(type(x))
    print(np.shape(x))

    plt.figure()
    plt.plot(x[0], label='position in x')
    plt.plot(x[1], label='position in y')
    plt.xlabel('time')
    plt.ylabel('MSE')
    plt.title('Mean Squared Error (MSE) of position')
    plt.legend()
    plt.show()


plot_MSE(1000, 0, 0, 0.1,0.1,0.001, 100)