#include <iostream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>

using namespace Eigen;

MatrixXd generate_true_values(int num_trials, double dt, double x_init, double y_init, double a_x, double a_y, bool x_y_only) {
    // matrix of floats of size 2xnum_trials (col # is dynamic)
    MatrixXd x(4,num_trials);
    Vector2d u(a_x, a_y);

    Vector4d init(x_init, y_init, 0, 0);
    x.col(0) = init;
    std::cout << x << std::endl;
    double dt_sq = dt*dt;

    Matrix4d A;
    A << 1, 0, dt, 0,
         0, 1, 0, dt, 
         0, 0, 0, 1,
         0, 0, 0, 1;
    
    MatrixXd B(4,2);
    B << 0.5*dt_sq, 0,
         0, 0.5*dt_sq,
         dt, 0,
         0, dt;

    for(int i = 1; i < num_trials; ++i)
        x.col(i) = A*x.col(i - 1) + B*u;

    
    // std::cout << time_int << std::endl;
    return x;
}

int main() {
    int num_trials = 10;
    double dt = 0.001;
    double x_init = 1;
    double y_init = 1;
    double a_x = 0.1;
    double a_y = 0.1;
    bool x_y_only = false;

    MatrixXd r = generate_true_values(num_trials, dt, x_init, y_init, a_x, a_y, x_y_only);
    std::cout << r << std::endl;
    return 0;
}