from Crypto import Random
from Crypto.Cipher import DES 
from cryptography.fernet import Fernet
import base64

def pad(s):
    return s + b"\0" * (DES.block_size - len(s) % DES.block_size)

# Создаем ключ и сохраняем его в файл 
def write_key(lenght_key=8):
    key = Fernet.generate_key()[:lenght_key]
    with open('crypto.key', 'wb') as key_file:
        key_file.write(key)

# Загружаем ключ 'crypto.key'
def load_key():
    return open('crypto.key', 'rb').read()
        
    
# Создаем вектор инициализации и сохраняем его в файл
def write_iv():
    iv = Random.new().read(DES.block_size)
    with open('crypto.iv', 'wb') as iv_file:
        iv_file.write(iv)

# Загружаем вектор инициализации 'crypto.iv'     
def load_iv():
    return open('crypto.iv', 'rb').read()

class SymmetricCipher():
    def __init__(self, file_name, key=None, iv=None):
        self.file_name = file_name
        self.cur_cipher = None
        if key != None:
            self.key = key
        else:
            self.key=write_key()
            
        if iv != None:
            self.iv = iv
        
    def encryptDES(self, message):
        message = pad(message)
        cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
        return self.iv + cipher.encrypt(message)

    def decryptDES(self, ciphertext):
        iv = ciphertext[:DES.block_size]
        cipher = DES.new(self.key, DES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[DES.block_size:])
        return plaintext.rstrip(b"\0")
    

    def encrypt_file(self, cipher):
        with open(self.file_name, 'rb') as fo:
            plaintext = fo.read()
        self.cur_cipher = cipher
        if cipher == 'DES':
            enc = self.encryptDES(plaintext)

        with open(self.file_name[:4] + 'sym_enc.txt', 'wb') as fo:
            fo.write(enc)
        return base64.b64encode(enc).decode('cp1251')

    def decrypt_file(self):
        with open(self.file_name[:4] + 'sym_enc.txt', 'rb') as fo:
            ciphertext = fo.read()
        cipher = self.cur_cipher
        if cipher == 'DES':
            dec = self.decryptDES(ciphertext)
            
        with open(self.file_name[:4] + 'sym_dec.txt', 'wb') as fo:
            fo.write(dec)
        return dec.decode('cp1251')

    
if __name__ == "__main__":
    # создадим и запишем в файл параметры
    write_key()
    write_iv()
    # загружаем параметры
    key = load_key()
    iv = load_iv()

    #s = SymmetricCipher(filename, key)
    #s.encrypt_file(cipher='Salsa20')
