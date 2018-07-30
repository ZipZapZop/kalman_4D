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

    a = plt.figure()
    plt.plot(x[0], label='Difference in x')
    plt.plot(x[1], label='Difference in y')
    plt.legend()
    plt.show()


# plot_differences(10000,0,0,0.1,0.1,0.001)


def mean_squared_error(num_trials, x_init, y_init, a_x, a_y, dt, q):
    all_diff = np.zeros((2, num_trials, q))
    # run error calculator for q trials, the more trials, the more accurate
    for i in range(0, q):
        # calculate all the differences for the qth trial, squares each one, and stores
        # each in an array for later use
        differences = calculate_differences(num_trials, x_init, y_init, a_x, a_y, dt)

        # squares each difference value and adds it to all previous difference values
        # stores the new value in the nth time interval
        for j in range(1, num_trials):
            all_diff[0, j, i] = all_diff[0, j - 1, i] + differences[0, j]**2
            all_diff[1, j, i] = all_diff[1, j - 1, i] + differences[1, j]**2

    MSE = np.zeros((2,num_trials))

    for i in range(0, num_trials):
        sum_x = 0
        sum_y = 0
        for j in range(0,q):
            sum_x = sum_x + all_diff[0, i, j]
            sum_y = sum_y + all_diff[1, i, j]
        
        MSE[0, i] = sum_x/num_trials
        MSE[1, i] = sum_y/num_trials

    return MSE

x = mean_squared_error(1000, 0, 0, 0.1,0.1,0.001, 100)
print(x)
print(type(x))
print(np.shape(x))

plt.figure()
plt.plot(x[0])
plt.plot(x[1])
plt.show()