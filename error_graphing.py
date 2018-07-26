import kalman
import generate_data
import numpy as np
import matplotlib.pyplot as plt


def calculate_differences(num_trials, x_init, y_init, a_x, a_y, dt):
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

x = calculate_differences(10000,0,0,0.1,0.1,0.001)
print(x)
print('\n')

a = plt.figure()
plt.plot(x[0], label='x')
plt.plot(x[1], label='y')
plt.legend()
plt.show()
