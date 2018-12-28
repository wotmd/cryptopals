from c10_Implement_CBC_mode import AES_cbc_decrypt, AES_cbc_encrypt
from Crypto.Util.strxor import strxor
import os




def Check_ASCII(plaintext):
	"""Returns true if all the characters of plaintext are ASCII compliant (ie are in the ASCII table)."""
	return all(c < 128 for c in plaintext)

def decrypt_and_check_admin(iv, key, ciphertext):
	"""Decrypts the ciphertext and: if the decrypted message is not ASCII compliant, raises an exception 
	and returns the bad plaintext; otherwise returns whether the characters ";admin=true;" are in the string.
	"""
	plaintext = AES_cbc_decrypt(ciphertext, key, iv)

	if not Check_ASCII(plaintext):
		raise Exception("The message is not valid", plaintext)

	return b';admin=true;' in plaintext

def get_key_from_insecure_cbc(iv, key):
	"""Recovers the key from the lazy encryption oracle using the key also as iv.
	The approach used is the simple one outlined in the challenge description.
	"""
	block_length = 16 #find_block_length(AES_cbc_decrypt)
	prefix_length =  0#find_prefix_length(AES_cbc_decrypt, block_length)

	# Create three different blocks of plaintext and encrypt their concatenation
	p_1 = 'A' * block_length
	p_2 = 'B' * block_length
	p_3 = 'C' * block_length
	p_4 = ";admin=true;" + "\x00"*4 
	ciphertext = AES_cbc_decrypt(p_1 + p_2 + p_3 + p_4, key, iv)

	# Force the ciphertext to be "C_1, 0, C_1"
	forced_ciphertext =  ciphertext[:block_length] 
	forced_ciphertext += b'\x00' * block_length 
	forced_ciphertext += ciphertext[:block_length]

	# Expect an exception from the lazy oracle
	try:
		decrypt_and_check_admin(iv, key, forced_ciphertext)
	except Exception as e:
		forced_plaintext = e.args[1]
		print(e)

		# Compute the key and return it
		# The first block of the plaintext will be equal to (decryption of c_1 XOR iv).
		# The last block of the plaintext will be equal to (decryption of c_1 XOR 0).
		# Therefore, to get the iv (which we know is equal to the key), we can just
		# xor the first and last blocks together.
		return strxor(forced_plaintext[:block_length], forced_plaintext[-block_length:])

	raise Exception("Was not able to hack the key")


def main():
	KEY = os.urandom(16)
	IV = KEY
	hacked_key = get_key_from_insecure_cbc(IV, KEY)
	
	# Check that the key was recovered correctly
	if KEY == hacked_key:
		print("success")


if __name__ == '__main__':
	main()