import random
from datetime import datetime
from random import randint
import PySimpleGUI as sg

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

def MillerRabin(n = 2, s = 50, numberOfIteration = 0): 
    for j in range(0, s):
        if (n < 2): n = 2
        a = randint(1, n - 1)
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
    numberOfIteration = 0
    start_time = datetime.now()
    for i in range(a,b):
        k = 0
        for j in listPrime:
            numberOfIteration += 1
            if (i % j == 0 and i // j != 1): 
                break
            else: 
                k+=1
        if (k == listPrime.__len__()):
            isPrime, numberOfIteration = MillerRabin(i, t, numberOfIteration)
            if (isPrime == False):
                primes.append(i)
    end_time = datetime.now() - start_time
    return primes, end_time, numberOfIteration

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def primitiveRoot(modulo):
    result=[]
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g

def primitiveRootList(modulo):
    result=[]
    start_time = datetime.now()
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        if result.__len__() == 100: break
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            result.append(g)
    return result, datetime.now() - start_time

def main():
    layout = [
    [sg.Text('Number of checks:'), sg.InputText()],
    [sg.Text('Number of bits:     '), sg.InputText()],
    [sg.Button('Generate prime number', expand_x=20)],
    [sg.Text('a '), sg.InputText()],
    [sg.Text('b '), sg.InputText()],
    [sg.Button('Generate prime numbers in range (a,b)', expand_x=20)],
    [sg.Text('Prime number(s):')],
    [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(88,10))]
    ]

    layout2 = [
    [sg.T('Number:\t'), sg.In(key='pr', size=(61, 1))],
    [sg.Button('Get primitive roots', expand_x=20)],
    [sg.Text('Primitive root:')],
    [sg.MLine(key='-ML2-'+sg.WRITE_ONLY_KEY, size=(88,10))]
    ]

    layout3 = [
    [sg.Button('Get', expand_x=20)],
    [sg.Text('Result:')],
    [sg.MLine(key='-ML3-'+sg.WRITE_ONLY_KEY, size=(88,10))]
    ]

    layoutOut = [
                    [   
                        sg.TabGroup(
                                        [[
                                            sg.Tab('Big prime number', layout, tooltip='tip'), 
                                            sg.Tab('Primitive root', layout2, tooltip='tip'),  
                                            sg.Tab('Diffie-Hellman', layout3, tooltip='tip')  
                                        ]], tooltip='TIP2'
                                    )
                    ] 
                ]


    window = sg.Window('Prime numbers', layoutOut, grab_anywhere=True, finalize=True)

    while True:                             # The Event Loop
        event, values = window.read()
        # print(event, values) #debug-
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Generate prime number':
            event, values = window.read()
            if values[0]=='' or values[1]=='':
                window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
                window['-ML1-'+sg.WRITE_ONLY_KEY].print('Incorrect input data')
            else:
                window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
                primeNumber, time, numberOfIteration = getPrimenumber(int(values[1]), int(values[0]))
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(primeNumber)
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(f" Time: {time}")
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(f" Number of iteration: {numberOfIteration}")
            
        if event == 'Generate prime numbers in range (a,b)':
            event, values = window.read()
            if values[2]=='' or values[3]=='':
                window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
                window['-ML1-'+sg.WRITE_ONLY_KEY].print('Incorrect input data')
            else:
                window['-ML1-'+sg.WRITE_ONLY_KEY].Update('')
                primeNumber, time, numberOfIteration = getPrimenumberInRange(int(values[2]), int(values[3]))
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(primeNumber)
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(f" Time: {time}")
                window['-ML1-'+sg.WRITE_ONLY_KEY].print(f" Number of iteration: {numberOfIteration}")
        
        if event == 'Get primitive roots':
            event, values = window.read()
            if values['pr']=='':
                window['-ML2-'+sg.WRITE_ONLY_KEY].Update('')
                window['-ML2-'+sg.WRITE_ONLY_KEY].print('Incorrect input data')
            else:
                window['-ML2-'+sg.WRITE_ONLY_KEY].Update('')
                pl, time = primitiveRootList(int(values['pr']))
                window['-ML2-'+sg.WRITE_ONLY_KEY].print(pl)
                window['-ML2-'+sg.WRITE_ONLY_KEY].print(f"Time: {time}")

        if event == 'Get':
            p, tmp1, tmp2 = getPrimenumber(10, 50)
            g = primitiveRoot(p)
            if (p == 1): p, tmp1, tmp2 = getPrimenumber(10, 50)
            alice_private = randint(1, p - 1)
            bob_private = randint(1, p - 1)

            # Generating public keys
            alice_public = pow(g, alice_private, p)
            bob_public = pow(g, bob_private, p)

            alice_key = (pow(bob_public, alice_private)) % p
            bob_key = (pow(alice_public, bob_private)) % p

            window['-ML3-'+sg.WRITE_ONLY_KEY].Update('')
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"n = {p}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"g = {g}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Alice private key = {alice_private}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Bob private key = {bob_private}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Alice public key = {alice_public}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Bob public key = {bob_public}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Alice key = {alice_key}")
            window['-ML3-'+sg.WRITE_ONLY_KEY].print(f"Bob key = {bob_key}")

main()