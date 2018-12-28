import base64

#Letter Distribution - Exterior Memory  http://www.macfreek.nl/memory/Letter_Distribution
freq = {
' ' : 18.28846265,
'E' : 10.26665037,
'T' : 7.51699827,
'A' : 6.53216702,
'O' : 6.15957725,
'N' : 5.71201113,
'I' : 5.66844326,
'S' : 5.31700534,
'R' : 4.98790855,
'H' : 4.97856396,
'L' : 3.31754796,
'D' : 3.28292310,
'U' : 2.27579536,
'C' : 2.23367596,
'M' : 2.02656783,
'F' : 1.98306716,
'W' : 1.70389377,
'G' : 1.62490441,
'P' : 1.50432428,
'Y' : 1.42766662,
'B' : 1.25888074,
'V' : 0.79611644,
'K' : 0.56096272,
'X' : 0.14092016,
'J' : 0.09752181,
'Q' : 0.08367550,
'Z' : 0.05128469,
}

#freq = {'a' : 8.167, 'b' : 1.492,'c' : 2.782,'d' : 4.253,'e' : 12.702,'f' : 2.228,'g' : 2.015,'h' : 6.094,'i' : 6.966,'j' : 0.153,'k' : 0.772,'l' : 4.025,'m' : 2.406,'n' : 6.749,'o' : 7.507,'p' : 1.929,'q' : 0.095,'r' : 5.987,'s' : 6.327,'t' : 9.056,'u' : 2.758,'v' : 0.978,'w' : 2.360,'x' : 0.150,'y' : 1.974,'z' : 0.074}

def alphabet_score(stringA):
	score = 0.0
	for c in stringA:
		c=c.upper()
		if c in freq:
			score+=freq[c]
	return score

def XOR_singleByte(str1, sbyte):
	str1 = str1.encode("hex")
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = sbyte
		result+= '{:02x}'.format(h1^h2)
	return result.decode("hex")

def XOR_with_Key(str1, Key):
	result = ""
	keylen=len(Key)
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = ord(Key[(i/2)%keylen])
		result+= '{:02x}'.format(h1^h2)
	return result

def Hamming_distance(str1, str2):
	d = 0
	for i in range(0, len(str1)):
		hd = ord(str1[i]) ^ ord(str2[i])
		while hd > 0:
			d += (hd & 0x1)
			hd = hd>>1
	return d

def get_candiate_key(cipher):
	normalized_average_d = []
	for KEY_LEN in range(2, 40):
		distance = 0.0
		n = (len(cipher)/(KEY_LEN))-1
		for bsize in range(0,len(cipher)-2*KEY_LEN,KEY_LEN):
			b1=cipher[bsize:bsize+KEY_LEN]
			b2=cipher[bsize+KEY_LEN:bsize+KEY_LEN*2]
			distance += Hamming_distance(b1, b2)
		normalized_average_d.append( (KEY_LEN, (distance/(n*KEY_LEN))) )
	normalized_average_d = sorted(normalized_average_d, key=lambda (x,y):y)
	
	return normalized_average_d
	
def get_candiate_key_length(cipher):
	normalized_average_d = []
	for KEY_LEN in range(2, 40):
		distance = 0.0
		n = (len(cipher)/(KEY_LEN))-1
		for bsize in range(0,len(cipher)-2*KEY_LEN,KEY_LEN):
			b1=cipher[bsize:bsize+KEY_LEN]
			b2=cipher[bsize+KEY_LEN:bsize+KEY_LEN*2]
			distance += Hamming_distance(b1, b2)
		normalized_average_d.append( (KEY_LEN, (distance/(n*KEY_LEN))) )
	normalized_average_d = sorted(normalized_average_d, key=lambda (x,y):y)
	
	return normalized_average_d
	
def get_keyString(cipher, KEY_LEN):
	keyString = ""
	for i in range(0, KEY_LEN):
		Max_score = 0.0
		score = 0.0
		key = 0
		for sbyte in range(0,255):
			nCaesar = ""
			for j in range(i, len(cipher), KEY_LEN):
				nCaesar += cipher[j]
			nomal_string = XOR_singleByte(nCaesar, sbyte)
			
			score = alphabet_score(nomal_string)
		
			if score > Max_score:
				Max_score = score
				key = sbyte
		keyString += chr(key)
	return keyString
	
def main():
	cipher = open("Challenge6.txt", "r").read().replace("\r\n","")
	cipher = base64.b64decode(cipher)

	normalized_average_d = get_candiate_key_length(cipher)

	print("candidate key length : ")
	for i in range(0,3):
		print(normalized_average_d[i])
	"""
	str1 = "this is a test"
	str2 = "wokka wokka!!!"
	print(Hamming_distance(str1, str2))
	"""
	KEY_LEN = normalized_average_d[0][0]
	print("\nKEY_LEN : %d " % KEY_LEN)
	
	keyString = get_keyString(cipher ,KEY_LEN)

	print("KeyString : "),
	print(keyString)

	print("\nPlaintext : ")
	plain = XOR_with_Key(cipher.encode("hex") ,keyString)
	plain = plain.decode("hex")

	print(plain)

if __name__ == '__main__':
    main()
