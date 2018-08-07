import matplotlib.pyplot as plt
import csv

def print_graph():
    with open('filtered_data_x.csv','r'):
        lines = [line.rstrip(' ') for line in open('filtered_data_x.csv')]
        lines = list(map(float, lines))
    
    plt.figure()
    plt.plot(lines,'k-',label='Kalman filter outputs')
    plt.legend()
    plt.title('')
    plt.show()

print_graph()