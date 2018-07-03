import base64
#from Crypto.Cipher import AES

f = open("Challenge8.txt", "r")
cipher_lines = f.readlines()
f.close()

BLOCK_SIZE = 16

for ciph in cipher_lines:
	ciph = ciph.strip().decode("hex")
	
	for i in range(0,len(ciph)-BLOCK_SIZE, BLOCK_SIZE):
		first_part = ciph[i:i+BLOCK_SIZE]
		front = ciph.find(first_part) 
		rear  = ciph.rfind(first_part)
		if front != rear:
			print("AES-ECB DETECT!!")
			print("cipher : "),
			print(ciph.encode("hex"))
			break
	"""	
	first_part, last_part = ciph[:BLOCK_SIZE], ciph[BLOCK_SIZE:]
	if first_part in last_part:
		print(ciph)
"""