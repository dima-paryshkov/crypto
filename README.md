# crypto
Prime Number Generation, Rabin-Miller Test, Finding Primitive Roots, RSA, DES

### Installation Process

    pip install pycrypto
    pip install base32hex 
    pip install PySimpleGUI
    pip install cryptography

### CGW.py

You can get a big prime number use `getPrimenumber(n, t = 50)`. n - a number of bits. t - a number of checks Miller Rabin.

You can check if a number is prime use `MillerRabin(n = 2, s = 50)`. n - your number, s - number of checking

You can get primitive root use `primitiveRoot(modulo)`. modulo - your number

### SymmetricCipher.py

Use `SymmetricCipher.py` you can get DES cipher:

Init:

`SC = SymmetricCipher.__init__(self, file_name, key=None, iv=None)`,  file_name - file with text.

Get key - `write_key(lenght_key=8)` and `load_key()`

Get iv - `write_iv()` and `load_iv()`

Encrypt use `SC.encrypt_file(cipher='DES')` 

Decrypt use `SC.decrypt_file()`

### CGW2var.py

Use `gcd(a, b)` to greatest common division

Get (e, n) and (d, n) for RSA use `generate_keypair(p, q)`, p and q - a big prime numbers

Get d for e use `multiplicative_inverse(e, phi)`, e - part of a open key, phi - Euler function (q - 1) * (p - 1)

Encrypt use `encrypt(pk, plaintext)`,  plaintext - your text, pk - public key

Decrypt use `decrypt(pk, ciphertext)`, cipher text - your text, pk - private key

There's mini interface.

If you press button Encrypt your text will be encrypt by DES and key of DES will Encrypt by RSA. 
You get detail of operatons of RSA and cipher