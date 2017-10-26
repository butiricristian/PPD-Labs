package com.company;

public class Runner implements Runnable{
    private int i1, i2, m, k;
    private int[][] matrix1;
    private int[][] matrix2;
    private int[][] matrixR;

    Runner(int i1, int i2, int m, int k, int[][] matrix1, int[][] matrix2, int[][] matrixR) {
        this.i1 = i1;
        this.i2 = i2;
        this.m = m;
        this.k = k;
        this.matrix1 = matrix1;
        this.matrix2 = matrix2;
        this.matrixR = matrixR;
    }

    @Override
    public void run() {
        for (int i = i1; i < i2; i++) {
            for (int j = 0; j < m; j++) {
                int sum = 0;
                for (int j2 = 0; j2 < k; j++) {
                    sum += matrix1[i][j] * matrix2[j][j2];
                }
                matrixR[i][j] = sum;
            }
        }
    }
}
