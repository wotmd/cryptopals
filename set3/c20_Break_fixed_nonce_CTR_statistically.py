from c18_Implement_CTR_mode import AES_CTR, XOR_with_Key
from c19_Break_fixed_nonce_CTR_mode_using_substitutions import get_keyString, Fix_keyString
from pwn import p64
from base64 import b64decode
import os

KEY = os.urandom(16)
nonce = p64(0)

BLOCK_SIZE = 16

def main():
	plainlist = open("Challenge20.txt", "r").readlines()
	plainlist = [b64decode(x) for x in plainlist]
	
	cipherlist = [AES_CTR(x, KEY, nonce) for x in plainlist]
	maxLen = max([len(x) for x in cipherlist])
	print("maxLen : %d " % maxLen)
	
	nColumnCipher = []
	for n in range(0, maxLen):
		nColumn = ""
		for c in cipherlist:
			if len(c) > n:
				nColumn += c[n]
		nColumnCipher.append(nColumn)
		
	keyString = get_keyString(nColumnCipher)
	keyString = Fix_keyString(keyString, cipherlist[0], "I'm rated \"R\"...this is a warning, ya better void / Poets are paranoid, DJ's D-stroyed")
	keyString = Fix_keyString(keyString, cipherlist[5], "Music's the clue, when I come your warned / Apocalypse How, when I'm done, ya gone!")
	keyString = Fix_keyString(keyString, cipherlist[59], "And we outta here / Yo, what happened to peace? / Peace")
	decrypt_list = [XOR_with_Key(ciph, keyString) for ciph in cipherlist]
	
	for i, decrpyt in enumerate(decrypt_list):
		print("%d : %s" %(i, decrpyt))
	
	# compare to original_plain & decrypt_plain
	for original, decrpyt in zip(plainlist, decrypt_list):
		print("o : " + original)
		print("d : " + decrpyt)
	
if __name__ == '__main__':
    main()

