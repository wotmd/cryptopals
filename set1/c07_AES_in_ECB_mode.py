import base64
from Crypto.Cipher import AES

f = open("Challenge7.txt", "r")
cipher = f.read().replace("\r\n","")
f.close()

cipher = base64.b64decode(cipher)

obj = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)
plain = obj.decrypt(cipher)

print("%s" % str(plain))


#https://pypi.org/project/pycrypto/
#openssl aes-128-ecb -d -in Challenge7_decode -out Challenge7_plain -K '59454C4C4F57205355424D4152494E45' -nosalt
