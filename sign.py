from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import base64

keyFile = open('cert.pem', 'rb')
key = RSA.importKey(keyFile.read())

cipher = Cipher_PKCS1_v1_5.new(key)
cipherText = cipher.encrypt('dZJrQkW32sXkeVF9G3Zc0jeO7UzCUEhs'.encode())
print(base64.b64encode(cipherText))