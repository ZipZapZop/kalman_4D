
#include <iostream>
#include <random>
#include <cmath>
#include <eigen3/Eigen/Dense>

using namespace Eigen;

int main() {
    MatrixXd x(4,8);
    Vector4d init(1, 1, 0, 0);
    x.col(0) = init;
    double dt = 0.001;
    Vector2d u(2, 2);

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

    Matrix4d H = Matrix4d::Identity();
    Matrix4Xd state(4, 8);
    state.col(0) = Vector4d(0, 0, 1, 1); 
    Matrix4d Q = Matrix4d::Zero(); 

    for(int i = 1; i < 8; ++i) { 
        state.col(i) = A*state.col(i - 1) + B*u;
        P = (A*P)*A.transpose();
        P = P + Q;

        Matrix4d K_num = P*(H.transpose());
        Matrix4d K_denom = (H*P);

    //    x.col(i) = A*x.col(i - 1) + B*;
    }
    std::cout << state << std::endl;
    return 0;
}
