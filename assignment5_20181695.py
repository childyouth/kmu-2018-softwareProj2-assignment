import time
import random

def fibo(n):
    if n <= 1:
        return n
    return fibo(n - 1) + fibo(n - 2)

def interFibo(n):
    fib1 = 1;
    fib2 = 1;
    ans = 1;
    for i in range(2,nbr):
        ans = fib1 + fib2
        fib1 = fib2
        fib2 = ans
    return ans

while True:
    nbr = int(input("Enter a number: "))
    if nbr == -1:
        break
    ts = time.time()
    fibonumber = fibo(nbr)
    ts = time.time() - ts
    interfibo_ts = time.time()
    ans = interFibo(nbr)
    interfibo_ts = time.time() - interfibo_ts

    print("Fibo(%d)=%d, time %.6f" %(nbr, fibonumber, ts))
    print("Fibo(%d)=%d, time %f" %(nbr, ans, interfibo_ts))