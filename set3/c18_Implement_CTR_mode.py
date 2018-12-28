from c10_Implement_CBC_mode import AES_ecb_encrypt
import base64
from pwn import p64
	
# from Crypto.Util.strxor import strxor
BLOCK_SIZE = 16

def XOR_with_Key(str1, Key):
	str1 = str1.encode("hex")
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = ord(Key[(i/2)%len(Key)])
		result+= '{:02x}'.format(h1^h2)
	return result.decode("hex")

def AES_CTR(data, key, nonce):
	xor_data = ""
	cnt = 0
	for i in range(0, len(data), BLOCK_SIZE):
		input = nonce + p64(cnt)
		xor_data += AES_ecb_encrypt(input, key)
		cnt+=1
	processing_data = XOR_with_Key(data, xor_data)
	return processing_data

def main():
	cipher = open("Challenge18.txt", "r").read().replace("\r\n","")
	cipher = base64.b64decode(cipher)

	nonce = p64(0)
	KEY = "YELLOW SUBMARINE"
	plain  = AES_CTR(cipher,KEY,nonce)
	
	print(plain)
	
	
if __name__ == '__main__':
    main()

