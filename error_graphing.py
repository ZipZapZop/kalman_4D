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
    # return filtered, true_vals
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


plot_differences(10000,0,0,0.1,0.1,0.001)