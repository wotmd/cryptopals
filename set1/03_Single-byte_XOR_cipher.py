import sys
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


enc = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def XOR(str1, sbyte):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = sbyte
		result+= '{:02x}'.format(h1^h2)
	return result

Max_score = 0.0
score = 0.0
plain = "none"
key = 1

for sbyte in range(0,255):
	result = XOR(enc, sbyte)
	nomal_string = result.decode("hex")
	
	score = alphabet_score(nomal_string)
	
	if score > Max_score:
		Max_score = score
		plain = nomal_string
		key = sbyte
		
	"""
	isStr = 1
	for test in nomal_string:
		if ord(test) < 0x20 or ord(test) > 126:
			isStr = -1
			break
	if isStr==1:
		print("%x" % sbyte),
		print(nomal_string)
	"""

print("Score 	: "+str(Max_score))
print("KeyByte	: %x" % key)
print("plaintext : %s" % plain)

# Cooking MC's like a pound of bacon
# key byte 58  // decimal 88