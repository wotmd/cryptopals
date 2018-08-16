from c10_Implement_CBC_mode import AES_ecb_encrypt, padding_pkcs7
from Crypto.Cipher import AES
from random import randint
import base64
import os

key = "4abc647688e6667c8c75bd5f1b508d13".decode("hex")
#key = os.urandom(16)

f = open("Challenge12.txt")
Suffix = base64.b64decode(f.read())
f.close()

def encryption_oracle(plain):
	plain = padding_pkcs7(plain+Suffix)
	return AES_ecb_encrypt(plain, key)

def find_block_size():
	c = encryption_oracle("")
	p = "A"
	while(True):
		cp = encryption_oracle(p)
		if(cp[len(p):]==c):
			return len(p)
		p+="A"

def ECB_check(cipher, block_size):
	for i in range(0,len(cipher)-block_size, block_size):
		first_part = cipher[i:i+block_size]
		front = cipher.find(first_part) 
		rear  = cipher.rfind(first_part)
		if front != rear and rear%block_size==0:
			return True
	return False

def get_next_byte(known_suffix, block_size):
	dic = {}
	feed = "\x00"*(block_size-1-(len(known_suffix)%block_size))

	for i in range(0,256):
		pt = feed + known_suffix + chr(i)
		ct = encryption_oracle(pt)[:len(pt)]
		dic[ct]=chr(i)
	ct = encryption_oracle(feed)[:len(feed + known_suffix)+1]
	if ct in dic:
		return dic[ct]
	else:
		return ""
	

if __name__ == '__main__':
	BLOCK_SIZE = find_block_size()
	if ECB_check(encryption_oracle("ABCD"*BLOCK_SIZE), BLOCK_SIZE) != True:
		exit(1)
	secret = ""
	while(True):
		one_byte = get_next_byte(secret, BLOCK_SIZE)
		if one_byte == "":
			break
		secret += one_byte
	print(secret)
	

