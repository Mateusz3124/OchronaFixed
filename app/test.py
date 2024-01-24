from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

def encrypt(plaintext,key, mode):
  encobj = AES.new(key, AES.MODE_GCM)
  ciphertext,authTag=encobj.encrypt_and_digest(plaintext)
  return(ciphertext,authTag,encobj.nonce)

def decrypt(ciphertext,key, mode):
  (ciphertext,  authTag, nonce) = ciphertext
  encobj = AES.new(key,  mode, nonce)
  return(encobj.decrypt_and_verify(ciphertext, authTag))
  
  
plaintext='4063330671623509'

value = "12345678"
key = PBKDF2(b"HGKTuwY11@!2"+value.encode(), b"PPGuvXffq")

ciphertext = encrypt(plaintext.encode(),key,AES.MODE_GCM)
h = []
stror = ""
for item in ciphertext:
  stror += b64encode(item).decode('utf-8') + ";"

stror = stror[0:len(stror)-1]

print(stror)

h = stror.split(";")
text = ()
for item in h:
  text += (b64decode(item),)

res= decrypt(text,key,AES.MODE_GCM)


print (res.decode())

#4063337151212679
#RacDUUT0AlRnGcZUKE8XBA==;ut7OCEmtdul8gZh57XpstA==;HCw3KJH2qvdjf1gvP4PVrw==
#ABC654321
#F/Mb5E3OoJr5;bE2zfn8bkZ4aebg+vX9hwQ==;DOyo4iSbK9hRt97s01zsLg==

#4063330671623509
#Jypa+kGBGNEM+IQGcwHTgA==;qyOTKRWbBeAMWVNz9IVw+w==;41CQoX9phbhl9sF9hQDGiA==
#ABC123456
#sdSCi+JKAHuq;QkTzpUA7ZfTni7jphZaKHQ==;3Xv2fjBYbtE7NfQ6hPLULA==