#include "generate_data.hpp"

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
