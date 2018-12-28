from c21_Implement_the_MT19937_Mersenne_Twister_RNG import MT19937
from Crypto.Util.strxor import strxor
from random import randint
from Crypto import Random
import struct

class MT19937StreamCipher:	#
	def __init__(self, key):
		self.rng = MT19937(key & 0xffff)

	def encrypt(self, plaintext):
		if len(plaintext) == 0:
			return ""
		keystream = ""
		while(True):
			keystream += struct.pack('<L', self.rng.uint32())
			if len(keystream) >= len(plaintext):
				break
		return strxor(plaintext.ljust(len(keystream),"\x00"), keystream)
		
	def decrypt(self, ciphertext):
		return self.encrypt(ciphertext)


def Crack_Seed(ciphertext, known_plaintext):
	for seed in range(0, 2**16):
		cipher = MT19937StreamCipher(seed)
		if known_plaintext in cipher.decrypt(ciphertext):
			return seed
	
		
def main():
	seed = randint(0, 2 ** 16 - 1)

	# Generate the plaintext which will be encrypted to get the password token
	random_prefix = Random.new().read(randint(0, 100)) + ";"
	known_plaintext = "MyriaBreak"
	random_suffix = ";" + "password_reset=true"	   # Let's make it more realistic

	ciphertext = MT19937StreamCipher(seed).encrypt(random_prefix + known_plaintext + random_suffix)
	guessed_seed = Crack_Seed(ciphertext, known_plaintext)

	# Check that the attack worked and print the recovered plaintext
	assert guessed_seed == seed
	print("> Decrypted password reset plaintext:", MT19937StreamCipher(seed).encrypt(ciphertext))


if __name__ == '__main__':
	main()