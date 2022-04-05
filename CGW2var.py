from email import charset
import random
from datetime import datetime
from random import randint
import PySimpleGUI as sg
from Crypto.Util import number

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

        if temp_phi == 1:
            return d + phi
    return d + phi

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    for e in range(3, phi):
        g = gcd(e, phi)
        d = multiplicative_inverse(e, phi)
        if g == 1 and e != d:
            break

    with open('public.txt', 'w') as key_file:
        key_file.write(str((e, n)))

    with open('private.txt', 'w') as key_file:
        key_file.write(str((d, n)))

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = []
    for char in plaintext:
        cipher.append(pow(ord(char), key, n))
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = ""
    for char in ciphertext:
        plain += chr(pow(char, key, n))
    return plain


def main():
    p = number.getPrime(128)
    q = number.getPrime(128)
    key_public, key_private = generate_keypair(p, q)
    message = "pizdec"
    encrypted_msg = encrypt(key_public, message)
    plain = decrypt(key_private, encrypted_msg)
    code = [ord(char) for char in message]
    print(plain)


main()
