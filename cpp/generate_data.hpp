#include <iostream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>
#include <fstream>

Eigen::MatrixXd generate_true_values(int num_trials, double dt, double x_init, double y_init, double a_x, double a_y);
Eigen::MatrixXd generate_noisy_values(int num_trials, double dt, double std_dev_x, double std_dev_y, double x_init, double y_init, double a_x, double a_y);
void export_noisy_to_csv(int num_trials, double dt, double std_dev_x, double std_dev_y, double x_init, double y_init, double a_x, double a_y);