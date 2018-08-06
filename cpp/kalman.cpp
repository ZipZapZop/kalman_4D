#include <iostream>
#include <eigen3/Eigen/Dense>
#include "generate_data.hpp"

using namespace Eigen;

MatrixXd kalman_filter(int num_trials, double x_init, double y_init, double a_x, double a_y) {
    double dt = 0.001;
    double dt_sq = dt*dt;

    // set std_dev_x and std_dev_y of sensors to 3m
    Matrix4Xd noisy_readings = generate_noisy_values(num_trials, dt, 3, 3, x_init, y_init, a_x, a_y);

    Matrix4d A;
    A << 1, 0, dt, 0,
         0, 1, 0, dt, 
         0, 0, 1, 0,
         0, 0, 0, 1;
    
    MatrixXd B(4,2);
    B << 0.5*dt_sq, 0,
         0, 0.5*dt_sq,
         dt, 0,
         0, dt;
    
    Matrix4d H = Matrix4d::Identity();

    // Init var of x and y are large because uncertain of original position.
    // Vel_x and vel_y are 0.1.
    // All covariances are equal to 0 as each state var is assumed independent.

    Matrix4d P;
    P << 500, 0, 0, 0,
         0, 500, 0, 0,
         0, 0, 0.1, 0,
         0, 0, 0, 0.1;
    
    Matrix4Xd variances(4, num_trials);


    Matrix4d Q = Matrix4d::Zero();  ////assuming a lack of process noise

    Matrix4d R;
    R << 9, 0, 0, 0,
         0, 9, 0, 0,
         0, 0, 0.01, 0,
         0, 0, 0, 0.01;

    Matrix4Xd state(4, num_trials);

    state.col(0) = Vector4d(0, 0, x_init, y_init); // init state
    Vector4d W = Vector4d::Zero(); // process noise is set to 0
    Vector2d u(a_x, a_y);
    MatrixXd Bu = B*u;
    for(int i = 1; i < num_trials; ++i) {
        state.col(i) = A*state.col(i - 1) + Bu + W;
        P = (A*P)*A.transpose() + Q;

        // gain
        Matrix4d K_num = P*(H.transpose());
        Matrix4d K_denom = (H*P);
        K_denom = K_denom*H.transpose();
        K_denom = K_denom * R;
        Matrix4d K = K_num*(K_denom.inverse());

        // update
        Vector4d innovation = noisy_readings.col(i) - H*state.col(i-1);
        state.col(i) = state.col(i) + K*innovation;
        P = (Matrix4d::Identity() - K*H)*P + Matrix4d::Zero();

        // save the variances at each step
        variances.col(i) = P.diagonal();
    }
    return state;

}

void filtered_to_csv(int num_trials, double x_init, double y_init, double a_x, double a_y) {
    MatrixXd filtered = kalman_filter(num_trials,  x_init, y_init, a_x, a_y);

    std::ofstream data_out;
    data_out.open("filtered_data_x.csv");

    for(int i = 0; i < num_trials; ++i)
        data_out << filtered(0,i) << '\n';
    data_out.close();

    data_out.open("filtered_data_y.csv");
    for(int i = 0; i < num_trials; ++i)
        data_out << filtered(1,i) << '\n';
    data_out.close();
}


int main() {
    int num_trials = 1000;
    double dt = 0.001;
    double x_init = 2;
    double y_init = 2;
    double std_dev_x = 3;
    double std_dev_y = 3;
    double a_x = 0.1;
    double a_y = 0.1;

    filtered_to_csv(num_trials,  x_init, y_init, a_x, a_y);
}