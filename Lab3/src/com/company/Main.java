package com.company;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class Main {

    private static int[][] matrixR = new int[10000][10000];

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

        int[][] matrix1 = new int[10000][10000];
        int[][] matrix2 = new int[10000][10000];
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
                futures.add(CompletableFuture.runAsync(new Runner(i*x, (i+1)*x, m, k, matrix1, matrix2, matrixR)));
            }
        }

        for(CompletableFuture f : futures){
            try {
                f.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }

        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                System.out.print(matrixR[i][j]);
            }
            System.out.println();
        }
    }
}
