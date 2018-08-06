import matplotlib.pyplot as plt
import csv

def print_graph():
    with open('test_x.csv','r') as d:
        lines = [line.rstrip(' ') for line in open('test_x.csv')]
        lines = list(map(float, lines))
    d.close()

    with open('true_x.csv','r') as e:
        reals = [real.rstrip(' ') for real in open('true_x.csv')]
        reals = list(map(float, reals))
    e.close()

    # add y plotting
    with open('true_y.csv','r') as f:
        reals = [real.rstrip(' ') for real in open('true_x.csv')]
        reals = list(map(float, reals))
    e.close()

    plt.figure()
    plt.plot(lines,label='Kalman filter outputs')
    plt.plot(reals)
    plt.legend()
    plt.title('')
    plt.show()

print_graph()