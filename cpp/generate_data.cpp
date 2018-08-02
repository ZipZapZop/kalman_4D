#include <iostream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>

using namespace Eigen;

MatrixXf generate_true_values(int num_trials, double dt, double x_init, double y_init, double a_x, double a_y, bool x_y_only) {
    std::cout << "generate_true_vals started\n";
    // matrix of floats of size 2xnum_trials (col # is dynamic)
    MatrixXf x(4,num_trials);
    // Vector2f u(a_x, a_y);

    Vector4f init(x_init, y_init, 0, 0);
    x.col(0) = init;

    std::cout << "generate_true_vals ended\n";
    return x;
}

int main() {
    int num_trials = 5;
    double dt = 0.001;
    double x_init = 1;
    double y_init = 1;
    double a_x = 0.1;
    double a_y = 0.1;
    bool x_y_only = false;

    MatrixXf r = generate_true_values(num_trials, dt, x_init, y_init, a_x, a_y, x_y_only);
    std::cout << r << std::endl;
    return 0;
}