#include <stdio.h>
#include <stdlib.h>

#define SIZE 64

int A[SIZE][SIZE];
int B[SIZE][SIZE];
int C[SIZE][SIZE];

int main() {
    int i, j, k;

    /* Initialize matrices */
    for (i = 0; i < SIZE; i++)
        for (j = 0; j < SIZE; j++) {
            A[i][j] = i + j;
            B[i][j] = i - j;
            C[i][j] = 0;
        }

    /* Matrix multiplication */
    for (i = 0; i < SIZE; i++)
        for (j = 0; j < SIZE; j++)
            for (k = 0; k < SIZE; k++)
                C[i][j] += A[i][k] * B[k][j];

    printf("Matrix multiplication complete. C[0][0] = %d\n", C[0][0]);
    return 0;
}