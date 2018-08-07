#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>
#include "generate_data.hpp"

using namespace Eigen;

const int num_trials = 1000;

MatrixXd kalman_filter() {
    double dt = 0.001;
    double a_x = 10;
    double a_y = 5;
    Vector2d u(a_x, a_y);   // accel in x and y

    Matrix4Xd noisy_readings = generate_noisy_values(num_trials, dt, 3, 3, 1, 1, a_x, a_y);

    double dt_sq = dt*dt;

    Matrix4d A;
    A << 1, 0, dt, 0,
         0, 1, 0, dt, 
         0, 0, 1, 0,
         0, 0, 0, 1;
    
    MatrixXd B(4,2);
    B << 0.5*dt_sq,  0,
         0,          0.5*dt_sq,
         dt,         0,
         0,          dt;
         
    Matrix4d P;
    P << 500, 0, 0, 0,
         0, 500, 0, 0,
         0, 0, 0.1, 0,
         0, 0, 0, 0.1;

    Matrix4d R;
    R << 9, 0, 0, 0,
         0, 9, 0, 0,
         0, 0, 0.01, 0,
         0, 0, 0, 0.01;

    Matrix4d H = Matrix4d::Identity();
    Matrix4Xd state(4, num_trials);
    state.col(0) = Vector4d(0, 0, 1, 1); 
    Matrix4d Q = Matrix4d::Zero(); 
    Matrix4d K;
    Vector4d innovation;

    for(int i = 1; i < num_trials; ++i) { 
        state.col(i) = A*state.col(i - 1) + B*u;
        P = (A*P)*A.transpose() + Q;

        Matrix4d K_num = P*(H.transpose());
        Matrix4d K_denom = (H*P);
        K_denom = H*K_denom*H.transpose();
        K_denom = K_denom + R;
        K = K_num*(K_denom.inverse());

        Vector4d innovation = noisy_readings.col(i) - H*state.col(i);
        state.col(i) += K*innovation;
        P = (Matrix4d::Identity() - (K*H))*P;
    }
    return state;
}

void filtered_to_csv() {
    MatrixXd filtered = kalman_filter();
    MatrixXd ideal = generate_true_values(num_trials, 0.001, 1, 1, 10, 5);

    std::ofstream data_out;
    data_out.open("test_x.csv");

    for(int i = 0; i < num_trials; ++i)
        data_out << filtered(0,i) << '\n';
    data_out.close();

    data_out.open("test_y.csv");
    for(int i = 0; i < num_trials; ++i)
        data_out << filtered(1,i) << '\n';
    data_out.close();

    data_out.open("ideal_x.csv");
    for(int i = 0; i < num_trials; ++i) {
        data_out << ideal(0, i) << '\n';
    }
    data_out.close();

    data_out.open("ideal_y.csv");
    for(int i = 0; i < num_trials; ++i) {
        data_out << ideal(1, i) << '\n';
    }
    data_out.close();
}

int main() {
    filtered_to_csv();
}