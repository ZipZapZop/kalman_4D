.PHONY: clean all
CFLAGS = -std=c++11

kalman: kalman.o
	g++ -o kalman kalman.o

clean:
	-rm kalman.o kalman

all:
	kalman
