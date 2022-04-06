import PySimpleGUI as sg
from Crypto.Util import number
import SymmetricCipher
import os
import base64

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

    for e in range(((p-10)*(q-10)), phi):
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

layout =  [
                [sg.T('p\t'), sg.In(key='p', size=(70, 1))],
                [sg.T('q\t'), sg.In(key='q', size=(70, 1))],
                [sg.T('n\t'), sg.In(key='n', size=(70, 1))],
                [sg.T('e\t'), sg.In(key='e', size=(70, 1))],
                [sg.T('d\t'), sg.In(key='d', size=(70, 1))],
                [sg.Text('_'  * 100, size=(30, 1)), sg.T('Initial data'), sg.Text('_'  * 100, size=(29, 1))], 
                [sg.T('Key\t'), sg.In(key='Key', size=(70, 1))],
                # [sg.T('IV\t'), sg.In(key='IV', size=(70, 1))],
                [sg.Push(), sg.Button('Generate new key'), sg.Button('Encrypt')],
                [sg.Text('_'  * 100, size=(70, 1))],
                [sg.Push(), sg.T('File content'), sg.Push()], 
                [sg.MLine(key='File_content', size=(78,5))], 
                [sg.Push(), sg.T('Encryption DES'), sg.Push(), sg.T('Encryption key RSA'), sg.Push()], 
                [sg.MLine(key='DES', size=(37,5)), sg.Push(), sg.MLine(key='RSA', size=(37,5))],
                [sg.Push(), sg.T('Decrypted file'), sg.Push()], 
                [sg.MLine(key='DecFile', size=(78,5))]
                ] 

window = sg.Window('Chiper RSA + DES', layout, grab_anywhere=True, finalize=True)

# key = SymmetricCipher.load_key()
# iv = SymmetricCipher.load_iv()
# window['Key'].Update(key)
# window['IV'].Update(base64.b64encode(iv).decode('cp1251'))

while True:
    event, values = window.read()  
    if event == sg.WIN_CLOSED:       
        break  

    if event == 'Generate new key':
        SymmetricCipher.write_key()
        SymmetricCipher.write_iv()
        
        key = SymmetricCipher.load_key()
        iv = SymmetricCipher.load_iv()
        window['Key'].Update(key) 
        # window['IV'].Update(base64.b64encode(iv).decode('cp1251'))

    if event == 'Encrypt':
        p = number.getPrime(128)
        q = number.getPrime(128)
        key_public, key_private = generate_keypair(p, q)

        window['p'].Update(p)
        window['q'].Update(q)
        window['e'].Update(key_public[0])
        window['d'].Update(key_private[0])
        window['n'].Update(key_public[1])


        key = SymmetricCipher.load_key()
        iv = SymmetricCipher.load_iv()

        encrypted_msg = encrypt(key_public, base64.b64encode(key).decode('cp1251'))
        plain = decrypt(key_private, encrypted_msg)

        SC = SymmetricCipher.SymmetricCipher(os.path.basename("SymCh.txt"), key, iv)
        a = open(os.path.basename("SymCh.txt"), 'r')
        f = a.read()
        a.close()
        window['File_content'].Update(f)

        window['DES'].Update(SC.encrypt_file(cipher='DES'))
        a = open(os.path.basename("encryptDES.txt"), 'w')
        a.write(SC.encrypt_file(cipher='DES'))
        a.close()

        window['RSA'].Update(encrypted_msg)
        a = open(os.path.basename("encryptKeyRSA.txt"), 'w')
        for item in encrypted_msg:
            a.write(str(item))
        a.close()

        window['DecFile'].Update(SC.decrypt_file())
        a = open(os.path.basename("decryptDES.txt"), 'w')
        a.write(SC.decrypt_file())
        a.close()
