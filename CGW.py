import random

def getPrimeNumberDefoultList(n):
    listprime=[]
     
    for i in range(2, 2000):
        f = True
        for j in listprime:
            if (i % j == 0):
                f = False
        if (f):
            listprime.append(i)

    return listprime

def toBinary(n):
    r = []
    # add 1 to the end
    r.append(1)
    n = n // 2
    while (n != 1):
        if (n // 2 == 1):
            r.append(1)
            return r
        r.append(n % 2)
        n = n // 2
    return r

def MillerRabin(n, s = 50):  
    b = toBinary(n - 1)
    for j in range(1, s + 1):
            a = random.randint(1, n - 1)
            d = 1
            for i in range(len(b) - 1, -1, -1):
                x = d
                d = (d * d) % n
                if d == 1 and x != 1 and x != n - 1:
                    return False # Составное
                if b[i] == 1:
                    d = (d * a) % n
                    if d != 1:
                        return False # Составное
                    return True # Простое

def getPrimenumber(n, t):
    isPrime = True
    listPrime = getPrimeNumberDefoultList(n)
    while (isPrime):
        primeNumber = random.getrandbits(n)
        for i in listPrime:
            if (primeNumber % i == 0):
                break
        isPrime =  MillerRabin(primeNumber, t)

    return primeNumber

def main():
    n = random.getrandbits(8)
    t = 5
    primeNumber = getPrimenumber(n, t)
    print(primeNumber)


main()