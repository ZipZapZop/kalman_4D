CC=g++

.PHONY: clean all
CFLAGS = -std=c++11 -msse2

kalman: 
	$(CC) -o kalman kalman.cpp generate_data.cpp
generate_data: generate_data.hpp
	$(CC) -o gen_data generate_data.cpp
clean:
	-rm kalman gen_data noisy_data_y.csv noisy_data_x.csv
all:
	kalman
