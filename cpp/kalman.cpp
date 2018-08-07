#include <eigen3/Eigen/Dense>
#include "generate_data.hpp"

using namespace Eigen;

/*  kalman_filter() applies a Kalman filter on the simulated noisy output from 
    generate_data.cpp. 
    There is assumed to be no noise in the prediction step of the filter and hence, the process 
    noise covariance matrix and the predicted state noise matrix are set to zero matrices.
    Measurements are taken at every 0.001 second (dt). This can be changed in the kalman.cpp 
    source.*/
MatrixXd kalman_filter(int num_trials, double x_init, double y_init, double std_dev_x, double std_dev_y, double a_x, double a_y) {
    // time interval of 0.001 seconds; filter is run with 1000 intervals (1 second total)
    double dt = 0.001;
    double dt_sq = dt*dt;

    Matrix4Xd noisy_readings = generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init, a_x, a_y);

    // relates previous step with current state; in this case, comes from physics equations
    Matrix4d A;
    A << 1, 0, dt, 0,
         0, 1, 0, dt, 
         0, 0, 1, 0,
         0, 0, 0, 1;
    
    // just like A, transforms between prev and curr state; also from physics equations
    MatrixXd B(4,2);
    B << 0.5*dt_sq,     0,
         0,             0.5*dt_sq,
         dt,            0,
         0,             dt;

    // Init var of x and y are large because uncertain of original position.
    // Vel_x and vel_y are 0.1.
    
    // All covariances are equal to 0 as each state var is assumed independent.
    // P diagonal is the variances each state var
    Matrix4d P;
    P << 500, 0, 0, 0,
         0, 500, 0, 0,
         0, 0, 0.01, 0,
         0, 0, 0, 0.01;

    // matrix to hold all states over the interval
    Matrix4Xd state(4, num_trials);
    state.col(0) = Vector4d(0, 0, x_init, y_init); // init state

    //assuming a lack of process noise
    Vector4d W = Vector4d::Zero();
    // process noise covariance is set to 0 as process noise is 0
    Matrix4d Q = Matrix4d::Zero();
    // This is just to convert between matrix dimensions
    Matrix4d H = Matrix4d::Identity();

    // to store the variances
    Matrix4Xd variances(4, num_trials);

    // sensor noise covariance matrix
    // std_dev_x and std_dev_y is 3m; std_dev_vx and std_dev_vy are sqrt(0.01)
    // this is definitely too low of a variance in real world scenario
    // don't think this will make too much of a difference in the prediction however
    Matrix4d R;
    R << 9, 0, 0, 0,
         0, 9, 0, 0,
         0, 0, 0.01, 0,
         0, 0, 0, 0.01;

    Vector2d u(a_x, a_y);
    MatrixXd Bu = B*u;
    for(int i = 1; i < num_trials; ++i) {
        // calculate new prediction state
        state.col(i) = A*state.col(i - 1) + Bu + W;
        P = (A*P)*A.transpose() + Q;

        // gain calculation
        Matrix4d K_num = P*(H.transpose());
        Matrix4d K_denom = (H*P);
        K_denom = H*K_denom*H.transpose();
        K_denom = K_denom + R;
        Matrix4d K = K_num*(K_denom.inverse());

        // update
        Vector4d innovation = noisy_readings.col(i) - H*state.col(i);
        state.col(i) += K*innovation;
        P = (Matrix4d::Identity() - (K*H))*P;

        // save the variances at each step
        variances.col(i) = P.diagonal();
    }
    return state;

}
/* Runs the filter and outputs .csv files with all state data over time */
void filtered_to_csv(int num_trials, double x_init, double y_init, double std_dev_x, double std_dev_y, double a_x, double a_y) {
    MatrixXd filtered = kalman_filter(num_trials,  x_init, y_init, std_dev_x, std_dev_y, a_x, a_y);
    MatrixXd ideal = generate_true_values(num_trials, 0.001, x_init, y_init, a_x, a_y);

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
    int num_trials = 1000;
    double x_init = 1;
    double y_init = 1;
    double std_dev_x = 3;
    double std_dev_y = 3;
    double a_x = 2;
    double a_y = 2;

    filtered_to_csv(num_trials, x_init, y_init, std_dev_x, std_dev_y, a_x, a_y);
}