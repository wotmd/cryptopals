from c18_Implement_CTR_mode import AES_CTR, XOR_with_Key
from c06_Break_repeating_key_XOR import alphabet_score, XOR_singleByte
from pwn import p64
from base64 import b64decode
import os

KEY = os.urandom(16)
nonce = p64(0)

BLOCK_SIZE = 16

def get_keyString(ciphers):
	keyString = ""
	for nColumnCipher in ciphers:
		Max_score = 0.0
		key = 0
		for sbyte in range(0,256):
			nomal_string = XOR_singleByte(nColumnCipher, sbyte)
			score = alphabet_score(nomal_string)
		
			if score > Max_score:
				Max_score = score
				key = sbyte
		keyString += chr(key)
	return keyString

def Fix_keyString(keyString, cipher, fix_plain):
	decrypt = XOR_with_Key(cipher, keyString)
	fix = XOR_with_Key(decrypt, fix_plain)
	fix_keyString = XOR_with_Key(keyString, fix)
	return fix_keyString
	
	
def main():
	plainlist = open("Challenge19.txt", "r").readlines()
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
	keyString = Fix_keyString(keyString, cipherlist[0], "I have met them at close of day")
	keyString = Fix_keyString(keyString, cipherlist[25], "This other his helper and friend")
	decrypt_list = [XOR_with_Key(ciph, keyString) for ciph in cipherlist]
	
	for i, decrpyt in enumerate(decrypt_list):
		print("%d : %s" %(i, decrpyt))
	
	# compare to original_plain & decrypt_plain
	for original, decrpyt in zip(plainlist, decrypt_list):
		print("o : " + original)
		print("d : " + decrpyt)

if __name__ == '__main__':
    main()

