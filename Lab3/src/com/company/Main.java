package com.company;

import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class Main {

    private static int[][] matrixR = new int[1000][1000];

    public static void main(String[] args) {
        Integer n = 0, k = 0, m = 0, w = 0;
        Scanner s = new Scanner(System.in);
        System.out.print("n= ");
        n = s.nextInt();
        System.out.print("k= ");
        k = s.nextInt();
        System.out.print("m= ");
        m = s.nextInt();
        System.out.print("Number of workers: ");
        w = s.nextInt();
        System.out.println(n.toString() + ", " + k.toString() + ", " + m.toString());

        int[][] matrix1 = new int[n][k];
        int[][] matrix2 = new int[k][m];
        Random randomGenerator = new Random();

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < k; j++) {
                matrix1[i][j] = randomGenerator.nextInt(10000);
            }
        }
        for (int i = 0; i < k; i++) {
            for (int j = 0; j < m; j++) {
                matrix2[i][j] = randomGenerator.nextInt(10000);
            }
        }

        ArrayList<CompletableFuture> futures = new ArrayList<>();
        int r = n % w;
        int x = n / w;
        for (int i = 0; i < w; i++) {
            if(r!=0) {
                futures.add(CompletableFuture.runAsync(new Runner(i*(x+1), (i+1)*(x+1), m, k, matrix1, matrix2, matrixR)));
                r--;
            }
            else{
                futures.add(CompletableFuture.runAsync(new Runner(i*x + n%w, (i+1)*x + n%w, m, k, matrix1, matrix2, matrixR)));
            }
        }

        Instant i1 = Instant.now();

        for(CompletableFuture f : futures){
            try {
                f.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }

        Instant i2 = Instant.now();

        System.out.println(i2.minusMillis(i1.toEpochMilli()).toEpochMilli());

//        for(int i=0;i<n;i++){
//            for(int j=0;j<m;j++){
//                System.out.print(String.valueOf(matrixR[i][j]) + " ");
//            }
//            System.out.println();
//        }
    }
}
