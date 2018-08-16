import os
from c10_Implement_CBC_mode import AES_ecb_encrypt, AES_cbc_encrypt, padding_pkcs7
from Crypto.Cipher import AES
from random import randint

BLOCK_SIZE = 16

def Oracle_Padding(data):
	# plus short random prefix and suffix."
	data = os.urandom(randint(5,10))+ data +os.urandom(randint(5,10))
	return data

def Oracle_Encrypt(plain):
	plain = Oracle_Padding(plain)
	plain = padding_pkcs7(plain)
	key = os.urandom(16)
	if randint(0,1) == 0:
		return "ECB", AES_ecb_encrypt(plain, key)
	else:
		IV = os.urandom(16)
		return "CBC", AES_cbc_encrypt(plain, key, IV)

def Detect_Mode(cipher):
	for i in range(0,len(cipher)-BLOCK_SIZE, BLOCK_SIZE):
		first_part = cipher[i:i+BLOCK_SIZE]
		front = cipher.find(first_part) 
		rear  = cipher.rfind(first_part)
		if front != rear and rear%BLOCK_SIZE==0:
			return "ECB"
	return "CBC"
	
	
if __name__ == '__main__':
	plain = bytes([0] * 47)
	key = os.urandom(16)
	
	for i in range(1000):
		mode,cipher = Oracle_Encrypt(plain)
		if mode == Detect_Mode(cipher):
			print(mode+" is Detect")
		else:
			print("Error")
			break
