
#include <iostream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>

using namespace Eigen;

int main() {
    MatrixXf x = MatrixXf::Zero(2,5);
    std::cout << x << std::endl;
    return 0;
}