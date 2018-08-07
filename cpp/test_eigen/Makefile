.PHONY: clean all
CFLAGS = -std=c++11 -Wall

test: test.o generate_data.o
	g++ $(CFLAGS) generate_data.o test.o -o test
test.o: test.cpp
	g++ $(CFLAGS) -c test.cpp
generate_data.o: generate_data.hpp generate_data.cpp
	g++ $(CFLAGS) -c generate_data.cpp
clean:
	rm -rf *.csv *.o test
