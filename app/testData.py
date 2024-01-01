from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode
from base64 import b64decode
import base64

def nullpadding(data, length=16):
    return data + b"\x00"*(length-len(data) % length) 
 
def encrypt(data,key, iv):
    data_padded = nullpadding(data)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = aes.encrypt(data_padded)
    return encrypted_data


def decrypt(data,key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = aes.decrypt(data)
    return encrypted_data


plaintext = b"ABC654321"
print(plaintext)
value = "87654321"
key = PBKDF2(b"HGKTuwY11@!2"+value.encode(), b"PPGuvXffq")
iv = get_random_bytes(16)
result = encrypt(plaintext,key,iv)

iv = b64encode(iv).decode('utf-8')
result = b64encode(result).decode('utf-8')
data = iv +";"+ result

print(data)

#INSERT INTO users (username, card, idNumber, account,loginCount) VALUES ('12345678', '4063330671623509', 'ABC123456','a23v567891011','0');
#INSERT INTO users (username, card, idNumber, account,loginCount) VALUES ('87654321', '4063337151212679', 'ABC654321', '1234567891011','0');

block = []

data = data.split(";")
iv = b64decode(data[0])
data = b64decode(data[1])

for i in range(int(len(data)/16)):
    block.append(data[i*16 : i*16 + 16])

key = PBKDF2(b"HGKTuwY11@!2"+value.encode(), b"PPGuvXffq")

result = []

result.append(decrypt(block[0], key, iv))

for i in range(len(block)-1):
    result.append(decrypt(block[i+1], key, block[i]))
data = b"".join(result)
data = data.rstrip(b"\x00")
print(data)
