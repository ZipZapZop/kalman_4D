import matplotlib.pyplot as plt
import csv

def print_graph():
    with open('test_x.csv','r') as d:
        filtered_x = [line.rstrip(' ') for line in open('test_x.csv')]
        filtered_x = list(map(float, filtered_x))
    d.close()

    with open('test_y.csv','r') as e:
        filtered_y = [line.rstrip(' ') for line in open('test_y.csv')]
        filtered_y = list(map(float, filtered_y))
    e.close()

    # add y plotting
    with open('ideal_x.csv','r') as f:
        ideal_x = [line.rstrip(' ') for line in open('ideal_x.csv')]
        ideal_x = list(map(float, ideal_x))
    f.close()

    with open('ideal_y.csv','r') as h:
        ideal_y = [line.rstrip(' ') for line in open('ideal_y.csv')]
        ideal_y = list(map(float, ideal_y))
    h.close()
    
    fig = plt.figure(num=1,figsize=(10, 10), dpi=100)
    
    plt.plot(filtered_x, label='Estimated values in x')
    plt.plot(filtered_y, label='Estimated values in y')
    plt.plot(ideal_x, label='Predicted values in x')
    plt.plot(ideal_y, label='Predicted values in y')
    plt.title('Filtered vs. Ideal values from a Kalman filter')
    fig.legend()
    
    plt.show()

print_graph()