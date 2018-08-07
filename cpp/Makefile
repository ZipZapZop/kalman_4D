CC=g++

.PHONY: clean all
CFLAGS = -std=c++11 -msse2 -Wall

kalman: kalman.o generate_data.o
	g++ $(CFLAGS) -o kalman kalman.o generate_data.o

kalman.o: kalman.cpp
	g++ $(CFLAGS) -c kalman.cpp

generate_data_main: generate_data_main.o generate_data.o
	g++ $(CFLAGS) generate_data_main.o generate_data.o -o generate_data

generate_data_main.o: generate_data_main.cpp
	g++ $(CFLAGS) -c generate_data_main.cpp

generate_data.o:  generate_data.hpp generate_data.cpp
	g++ $(CFLAGS) -c generate_data.cpp

clean:
	-rm kalman *.csv *.o

# clean generate_data:
# 	-rm generate_data.o generate_data noisy_data_x.csv noisy_data_y.csv

all:
	kalman
