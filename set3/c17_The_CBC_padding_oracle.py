from c10_Implement_CBC_mode import *
from Crypto.Random import random
import base64
import os

BLOCK_SIZE = 16

def encrypt_oracle(plain, key, IV):
	plain = padding_pkcs7(plain)
	enc = AES_cbc_encrypt(plain, key, IV)
	return enc

def CheckValidPadding(cipher, key, IV):
	plain = AES_cbc_decrypt(cipher, key, IV)
	try:
		p = unpadding_pkcs7(plain)
		return True
	except ValueError:
		return False
		
def get_nextBlock_decrypt(cipher, iv, key):
	knownP = ""
	for padding_len in range(1,BLOCK_SIZE+1):
		candiP = ""
		for i in range(256):
			makeIV = "\x00"*(BLOCK_SIZE-padding_len) + chr(i ^ ord(iv[-padding_len]) ^ padding_len)
			for j in range(0,len(knownP)):
				makeIV += chr(ord(iv[len(makeIV)]) ^ ord(knownP[j]) ^ padding_len)
			if CheckValidPadding(cipher,key,makeIV):
				candiP += chr(i)
		if len(candiP) != 1:
			print(candiP)
			print("No!!")
			knownP = candiP[0] + knownP
		else:
			knownP = candiP + knownP
	return knownP
	
def OraclePaddingAttack(cipher, key, IV):
	KnownP = ""
	ciphers = [IV]
	for i in range(0, len(cipher), BLOCK_SIZE):
		ciphers.append(cipher[i:i+BLOCK_SIZE])
	for i, c in enumerate(ciphers[1:]):
		preIV = ciphers[i]
		KnownP += get_nextBlock_decrypt(c, preIV, key)
	return unpadding_pkcs7(KnownP)

if __name__ == '__main__':
	strings = open("Challenge17.txt").read().split("\r\n")
	KEY = os.urandom(16)
	IV = os.urandom(16)
	plain = base64.b64decode(random.choice(strings))
	
	cipher = encrypt_oracle(plain, KEY, IV)
	decode_plain =  OraclePaddingAttack(cipher, KEY, IV)
	
	print(decode_plain)
	
	

