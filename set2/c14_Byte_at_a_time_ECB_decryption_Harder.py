from c12_Byte_at_a_time_ECB_decryption_Simple import *
from Crypto.Cipher import AES
from random import randint
import base64
import os

Prefix = os.urandom(randint(8, 48))

def prefix_encryption_oracle(plain):
	plain = Prefix+plain
	return encryption_oracle(plain)
	
def find_AAA(encryption_oracle, BLOCK_SIZE):
	p = "A"*BLOCK_SIZE*4
	c = encryption_oracle(p)
	for i in range(0,len(c)-BLOCK_SIZE, BLOCK_SIZE):
		first_part = c[i:i+BLOCK_SIZE]
		front = c.find(first_part) 
		rear  = c.rfind(first_part)
		if front != rear and rear%BLOCK_SIZE==0:
			return first_part, front
	return "", 0
	
def find_Prefix_size(encryption_oracle, BLOCK_SIZE):
	AAA, index = find_AAA(encryption_oracle, BLOCK_SIZE)
	if AAA == "":
		raise Exception('Not using ECB')
	pre_cp = encryption_oracle("")
	p = "A"
	while(True):
		cp = encryption_oracle(p)
		if AAA in cp:
			modsize = BLOCK_SIZE - len(p)
			return index+modsize
			break
		p+="A"
			

if __name__ == '__main__':
	BLOCK_SIZE = find_block_size(prefix_encryption_oracle)
	PREFIX_SIZE = find_Prefix_size(prefix_encryption_oracle, BLOCK_SIZE)
	print("BLOCK_SIZE  : %d" % BLOCK_SIZE)
	print("PREFIX_SIZE : %d" % PREFIX_SIZE)
	secret = ""
	while(True):
		one_byte = get_next_byte(prefix_encryption_oracle, secret, BLOCK_SIZE, PREFIX_SIZE)
		if one_byte == "":
			break
		secret += one_byte
	print(secret)


