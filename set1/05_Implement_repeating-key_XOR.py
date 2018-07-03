import sys

def alphabet_score(stringA):
	score = 0.0
	for c in stringA:
		c=c.upper()
		if c in freq:
			score+=freq[c]
	return score

def XOR(str1, sbyte):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = sbyte
		result+= '{:02x}'.format(h1^h2)
	return result
	
def XOR_with_Key(str1, Key):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = ord(Key[(i/2)%len(Key)])
		result+= '{:02x}'.format(h1^h2)
	return result

	
	
f = open("Challenge5.txt", "r")
plain = f.read()
f.close()

key = "ICE"

result = XOR_with_Key(plain.encode("hex"), key)
print(result)


