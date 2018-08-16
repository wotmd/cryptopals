import base64
from Crypto.Cipher import AES
	
BLOCK_SIZE = 16

def XOR_with_Key(str1, Key):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = ord(Key[(i/2)%len(Key)])
		result+= '{:02x}'.format(h1^h2)
	return result.decode("hex")

def padding_pkcs7(block):	# util.padPKCS7(s, 16)
	n_padd = (BLOCK_SIZE - (len(block)%BLOCK_SIZE)) #% BLOCK_SIZE
	pad = chr(n_padd)*n_padd
	return block+pad

def unpadding_pkcs7(block):
	len_b = len(block)
	n_padd = ord(block[-1])
	for c in range(0, n_padd):
		if(n_padd != ord(block[len_b-1-c])):
			return block
		
	unpad_block = block[:-n_padd]
	return unpad_block
	
	
def AES_ecb_encrypt(plain, key):
	obj = AES.new(key, AES.MODE_ECB)
	cipher = obj.encrypt(plain)
	
	return cipher

def AES_ecb_decrypt(cipher, key):
	obj = AES.new(key, AES.MODE_ECB)
	plain = obj.decrypt(cipher)
	return plain
	
def AES_cbc_encrypt(plain, key, IV):
	ciphertext = ""
	pre_block = IV
	for i in range(0, len(plain), BLOCK_SIZE):
		current_block = plain[i:i+BLOCK_SIZE]
		input = XOR_with_Key(current_block.encode("hex"),pre_block)
		cipher = AES_ecb_encrypt(input, key)
		ciphertext += cipher
		pre_block = cipher
	
	return ciphertext


def AES_cbc_decrypt(cipher, key, IV):
	ciphertext = cipher
	plaintext = ""
	pre_block = IV
	for i in range(0, len(ciphertext), BLOCK_SIZE):
		current_block = ciphertext[i:i+BLOCK_SIZE]
		output = AES_ecb_decrypt(current_block, key)
		plain = XOR_with_Key(output.encode("hex"),pre_block)
		plaintext += plain
		pre_block = current_block
	
	return plaintext

def main():
	f = open("Challenge10.txt", "r")
	cipher = f.read().replace("\r\n","")
	f.close()

	cipher = base64.b64decode(cipher)

	IV = "\x00"*BLOCK_SIZE
	KEY = "YELLOW SUBMARINE"
	plain  = AES_cbc_decrypt(cipher,KEY,IV)
	plain = unpadding_pkcs7(plain)
	
	print(plain)
	
	
if __name__ == '__main__':
    main()


#https://pypi.org/project/pycrypto/
