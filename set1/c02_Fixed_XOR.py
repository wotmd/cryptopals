import sys

if len(sys.argv) < 3:
	print("usage : 02_Fixed_XOR str1 str2")
	exit(1)

def XOR(str1, str2):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = int(str2[i:i+2],16)
		result+= '{:02x}'.format(h1^h2)
	return result
		
	
str1 = sys.argv[1]
str2 = sys.argv[2]

xor = XOR(str1, str2)

print(xor)