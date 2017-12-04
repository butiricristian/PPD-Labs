using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Lab3_CS
{

    public class Runner
    {
        private int i1, i2, m, k;
        private int[,] matrix1;
        private int[,] matrix2;
        private int[,] matrixR;

        private ManualResetEvent doneEvent;

        public Runner(int i1, int i2, int m, int k, int[,] matrix1, int[,] matrix2, int[,] matrixR, ManualResetEvent doneEvent)
        {
            this.i1 = i1;
            this.i2 = i2;
            this.m = m;
            this.k = k;
            this.matrix1 = matrix1;
            this.matrix2 = matrix2;
            this.matrixR = matrixR;
            this.doneEvent = doneEvent;
        }

        public void ThreadPoolCallback(Object threadContext)
        {
            for (int i = i1; i < i2; i++)
            {
                for (int j = 0; j < m; j++)
                {
                    int sum = 0;
                    for (int j2 = 0; j2 < k; j2++)
                    {
                        sum += matrix1[i, j2] * matrix2[j2, j];
                    }
                    matrixR[i, j] = sum;
                }
            }
            doneEvent.Set();
        }
    }


    class Program
    {
        static void Main(string[] args)
        {
            int n = 0, k = 0, m = 0, w = 0;
            Console.Write("n= ");
            n = Int32.Parse(Console.ReadLine());
            Console.Write("k= ");
            k = Int32.Parse(Console.ReadLine());
            Console.Write("m= ");
            m = Int32.Parse(Console.ReadLine());
            Console.Write("Number of workers: ");
            w = Int32.Parse(Console.ReadLine());

            int[,] matrix1 = new int[n, k];
            int[,] matrix2 = new int[k, m];
            int[,] matrixR = new int[n, m];
            Random randomGenerator = new Random();

            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < k; j++)
                {
                    matrix1[i, j] = randomGenerator.Next(10000);
                }
            }
            for (int i = 0; i < k; i++)
            {
                for (int j = 0; j < m; j++)
                {
                    matrix2[i, j] = randomGenerator.Next(10000);
                }
            }

            int r = n % w;
            int x = n / w;
            ManualResetEvent[] manualResetEvents = new ManualResetEvent[w];

            for (int i = 0; i < w; i++)
            {
                manualResetEvents[i] = new ManualResetEvent(false);
                if (r != 0)
                {
                    ThreadPool.QueueUserWorkItem(new Runner(i * (x + 1), (i + 1) * (x + 1), m, k, matrix1, matrix2, matrixR, manualResetEvents[i]).ThreadPoolCallback);
                    r--;
                }
                else
                {
                    ThreadPool.QueueUserWorkItem(new Runner(i * x + n%w, (i + 1) * x + n % w, m, k, matrix1, matrix2, matrixR, manualResetEvents[i]).ThreadPoolCallback);
                }
            }

            DateTime t1 = DateTime.Now;

            WaitHandle.WaitAll(manualResetEvents);

            DateTime t2 = DateTime.Now;

            Console.WriteLine((t2 - t1).Milliseconds);

            //for (int i = 0; i < n; i++)
            //{
            //    for (int j = 0; j < m; j++)
            //    {
            //        Console.Write(matrixR[i, j].ToString() + " ");
            //    }
            //    Console.WriteLine();
            //}
        }
    }
}
