CC=g++

.PHONY: clean all
CFLAGS = -std=c++11

kalman: 
	$(CC) -o kalman kalman.cpp generate_data.cpp
generate_data:
	$(CC) -o gen_data generate_data.cpp
clean:
	-rm kalman.o generate_data.o kalman gen_data
all:
	kalman
