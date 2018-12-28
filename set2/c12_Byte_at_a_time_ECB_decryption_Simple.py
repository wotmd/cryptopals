from c10_Implement_CBC_mode import AES_ecb_encrypt, padding_pkcs7
from Crypto.Cipher import AES
from random import randint
import base64
import os

key = os.urandom(16)
Suffix = base64.b64decode(open("Challenge12.txt").read())

def encryption_oracle(plain):
	plain = padding_pkcs7(plain+Suffix)
	return AES_ecb_encrypt(plain, key)

def find_block_size(encryption_oracle):
	pre_cp = encryption_oracle("")
	p = "A"
	while(True):
		cp = encryption_oracle(p)
		size = len(cp)-len(pre_cp)
		if size != 0:
			return size
		p+="A"

def ECB_check(cipher, block_size):
	for i in range(0,len(cipher)-block_size, block_size):
		first_part = cipher[i:i+block_size]
		front = cipher.find(first_part) 
		rear  = cipher.rfind(first_part)
		if front != rear and rear%block_size==0:
			return True
	return False

def get_next_byte(encryption_oracle, known_suffix, block_size, prefix_size):
	dic = {}
	feed = "\x00"*(block_size-(prefix_size%block_size))
	feed += "\x00"*(block_size-1-(len(known_suffix)%block_size))

	for i in range(0,256):
		pt = feed + known_suffix + chr(i)
		ct = encryption_oracle(pt)[:len(pt)+prefix_size]
		dic[ct]=chr(i)
	ct = encryption_oracle(feed)[:len(feed + known_suffix)+1+prefix_size]
	if ct in dic:
		return dic[ct]
	else:
		return ""
	

if __name__ == '__main__':
	BLOCK_SIZE = find_block_size(encryption_oracle)
	if ECB_check(encryption_oracle("ABCD"*BLOCK_SIZE*2), BLOCK_SIZE) != True:
		exit(1)
	secret = ""
	while(True):
		one_byte = get_next_byte(encryption_oracle, secret, BLOCK_SIZE, 0)
		if one_byte == "":
			break
		secret += one_byte
	print(secret)
	

