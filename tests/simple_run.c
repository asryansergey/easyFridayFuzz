#include<stdio.h>
#include<stdlib.h>

int main(int argc, char** argv) {

    FILE* input_file = fopen(argv[1], "r");
    char buff[100];
    int count = 0;
    fscanf(input_file, "%s", buff);
    if (buff[0] == 'o')
        count++;
    if (buff[1] == 'k')
        count++;
    if (count == 2)
        abort();
    return 0;
}