import random
from datetime import datetime

def getPrimeNumberDefoultList():
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
    while (n > 0):
        r.append(n % 2)
        n = n / 2
        return r

def MillerRabin(n, s = 50, numberOfIteration = 0): 
    for j in range(0, s):
        a = random.randint(1, n - 1)
        b = toBinary(n - 1)
        d = 1
        for i in range(len(b) - 1, -1, -1):
            x = d
            numberOfIteration += 1
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return True, numberOfIteration # Составное
            if b[i] == 1:
                d = (d * a) % n
                if d != 1:
                    return True, numberOfIteration # Составное
    return False, numberOfIteration # Простое

def getPrimenumber(n, t = 50):
    isPrime = True
    listPrime = getPrimeNumberDefoultList()
    numberOfIteration = 0
    start_time = datetime.now()
    while (isPrime):
        primeNumber = random.getrandbits(n)
        if (n % 2 == 0):
            n += 1
        k = 0
        for i in listPrime:
            numberOfIteration += 1
            if (primeNumber % i == 0): break
            else: k+=1
        lenght = listPrime.__len__()
        if (k == lenght):
            isPrime, numberOfIteration =  MillerRabin(primeNumber, t, numberOfIteration)

    end_time = datetime.now() - start_time
    return primeNumber, end_time, numberOfIteration

def getPrimenumberInRange(a, b, numberOfIteration = 0, t = 50):
    primes = []
    listPrime = getPrimeNumberDefoultList()
    for i in range(a,b):
        k = 0
        for j in listPrime:
            numberOfIteration += 1
            if (i % j == 0): 
                break
            else: 
                k+=1
        if (k == listPrime.__len__()):
            isPrime, numberOfIteration = MillerRabin(i, t, numberOfIteration)
            if (isPrime == False):
                primes.append(i)
    return primes



def main():
    n = 256
    t = 50
    primeNumber, time, numberOfIteration = getPrimenumber(n, t)
    print(primeNumber)
    print(time)
    print(numberOfIteration)

main()