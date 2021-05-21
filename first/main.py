import time

# Utility functions
def timeit(func, *args):
    ini = time.time()
    val = func(*args)
    fin = time.time()
    return (fin - ini) * 1000
def timeit_averg(func, n, *args):
    averg = 0
    for i in range(n):
        averg += timeit(func, *args)
    averg = averg / n
    print(f'{func.__name__}\t{averg:.5f} ms')


# Recursion methods
def fib_onerecur(n):
    if n < 2:
        return 1
    return fib_onerecur(n-1) + fib_onerecur(n-2)
def fib_allrecur(n):
    for a in range(n):
        fib_onerecur(a)

# Iterative methods
def fib_iter(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b

# Generator methods
def fib_gen():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b
def fib_gen_print(n):
    gen = fib_gen()
    for _ in range(n):
        next(gen)


# Main
if __name__ == "__main__":
    r = int(input("Repetitions: "))
    n = int(input("How many: "))
    timeit_averg(fib_onerecur, r, n)
    timeit_averg(fib_allrecur, r, n)
    timeit_averg(fib_iter, r, n)
    timeit_averg(fib_gen_print, r, n)
