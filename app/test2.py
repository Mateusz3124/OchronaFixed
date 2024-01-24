from hashlib import blake2b
secret_key = b"BKgasdqw3#!@#412fuiu[][fdDAgafhu3424fsfds;''[54]"
h = blake2b(digest_size=30, salt=b"87654321", key=secret_key)
h.update("22134.11".encode())
value = "22134.11" + "," +h.hexdigest()
print(value)
valu = value.split(",")

h = blake2b(digest_size=30, salt=b"12345678", key=secret_key)
h.update("25121.21".encode())
p = h.hexdigest()

