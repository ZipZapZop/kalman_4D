import matplotlib.pyplot as plt
import csv

def print_graph():
    with open('test_x.csv','r') as d:
        filtered_x = [line.rstrip(' ') for line in open('test_x.csv')]
        filtered_x = list(map(float, filtered_x))
    d.close()

    with open('test_y.csv','r') as e:
        filtered_y = [line.rstrip(' ') for line in open('true_x.csv')]
        filtered_y = list(map(float, filtered_y))
    e.close()

    # add y plotting
    with open('true_x.csv','r') as f:
        ideal_x = [line.rstrip(' ') for line in open('true_x.csv')]
        ideal_x = list(map(float, ideal_x))
    f.close()

    with open('true_y.csv','r') as h:
        ideal_y = [line.rstrip(' ') for line in open('true_y.csv')]
        ideal_y = list(map(float, ideal_y))
    h.close()
    
    fig = plt.figure(num=1,figsize=(12, 10), dpi=100)
    
    ax1 = fig.add_subplot(112)
    plt.plot(filtered_x, label='Estimated values')
    plt.plot(ideal_x, label='Predicted values')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.set_title('x position')

    ax2 = fig.add_subplot(212)  # y values
    plt.plot(filtered_y)
    plt.plot(ideal_y)
    ax2.set_title('y position')

    fig.legend(handles, labels)     # handles and labels for ax2, ax3, ax4 are same as for ax1
    fig.subplots_adjust(hspace=.2,wspace=.2)
    
    plt.show()

print_graph()