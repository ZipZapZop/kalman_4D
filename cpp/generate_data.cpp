#include "generate_data.hpp"

using namespace Eigen;

MatrixXd generate_true_values(int num_trials, double dt, double x_init, double y_init, double a_x, double a_y) {
    // matrix of floats of size 2xn
    MatrixXd x(4,num_trials);
    Vector2d u(a_x, a_y);

    Vector4d init(x_init, y_init, 0, 0);
    x.col(0) = init;
   double dt_sq = dt*dt;

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

    for(int i = 1; i < num_trials; ++i)
        x.col(i) = A*x.col(i - 1) + B*u;

    return x;
}

MatrixXd generate_noisy_values(int num_trials, double dt, double std_dev_x, double std_dev_y, double x_init, double y_init, double a_x, double a_y) {
    std::random_device rd;
    std::mt19937 gen(rd());

    std::default_random_engine generator;
    std::normal_distribution<> Nx(0, std_dev_x);
    std::normal_distribution<> Ny(0, std_dev_y);

    MatrixXd true_vals = generate_true_values(num_trials, dt, x_init, y_init, a_x, a_y);

    MatrixXd sensor_values(4,num_trials);

    for(int i = 0; i < num_trials; ++i) {
        sensor_values(0,i) = true_vals(0, i) + Nx(gen);
        sensor_values(1,i) = true_vals(1, i) + Ny(gen);
        sensor_values(2,i) = true_vals(2, i) + Nx(gen);  
        sensor_values(3,i) = true_vals(3, i) + Ny(gen);
    }

    return sensor_values;
} 

void export_noisy_to_csv(int num_trials, double dt, double std_dev_x, double std_dev_y, double x_init, double y_init, double a_x, double a_y) {
    MatrixXd r = generate_noisy_values(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init, a_x, a_y);

    std::ofstream data_out;
    data_out.open("noisy_data_x.csv");
    for(int i = 0; i < num_trials; ++i)
        data_out << r(0,i) << '\n';
    data_out.close();

    data_out.open("noisy_data_y.csv");
    for(int i = 0; i < num_trials; ++i)
        data_out << r(1,i) << '\n';
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
    export_noisy_to_csv(num_trials, dt, std_dev_x, std_dev_y, x_init, y_init, a_x, a_y);
}


