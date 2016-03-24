
#include <iostream>

int main() {

  typedef uint unsigned short int;

  const uint numRep = 3;

  for( uint i = 0; i < numRep; ++i ) {
    std::cout << "Hello, World!" << std::endl;
  }

  return 0;

}
