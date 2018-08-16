import base64
import sys

if len(sys.argv) < 2:
	print("usage : 01_Convert_hex_to_base64.py [string]")
	exit(1)

hexstring = sys.argv[1]

nomal_string = hexstring.decode("hex")

enc = base64.b64encode(nomal_string)

#print(nomal_string)
print(enc)