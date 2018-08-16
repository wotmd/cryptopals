import base64

BLOCK_SIZE = 20

def padding_pkcs7(block):
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
	
	
plaintext = "YELLOW SUBMARINE"
padding_plain = padding_pkcs7(plaintext)

print(repr(padding_plain))

unpadding_plain = unpadding_pkcs7(padding_plain)
print(repr(unpadding_plain))