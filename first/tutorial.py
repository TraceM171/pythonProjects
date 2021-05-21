# Armstrong numbers
def isArmstrong(n):
    nth = len(str(n))
    i = n
    nthSum = 0
    while i != 0:
        nthSum += (i % 10) ** nth
        i = i // 10
    return n == nthSum
def armstrongNumbers():
    n = int(input("How many amstrong numbers: "))
    for i in range(n):
        if isArmstrong(i):
            print(i)

# Number triangles
def numberTriangles():
    rows = int(input("How many rows: "))
    for i in range(rows):
        print(*list(range(1, i + 2)), sep=' ')
def numberTriangles2():
    rows = int(input("How many rows: "))
    for i in range(rows):
        print(*list([i + 1 for _ in range(i + 1)]), sep=' ')
    

if __name__ == "__main__":
    numberTriangles()
