import matplotlib.pyplot as plt
import csv

def print_graph():
    with open('noisy_data_x.csv','r') as d:
        lines = [line.rstrip(' ') for line in open('noisy_data_x.csv')]
        lines = list(map(float, lines))
            
    plt.figure()
    plt.plot(lines,'k-',label='Kalman filter outputs')
    plt.legend()
    plt.title('Kalman filter vs the true value')
    plt.show()

print_graph()