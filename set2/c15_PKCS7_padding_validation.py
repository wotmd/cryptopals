from c10_Implement_CBC_mode import unpadding_pkcs7

def main():
	p = "ICE ICE BABY"
	c= unpadding_pkcs7('ICE ICE BABY\x04\x04\x04\x04')
	try:
		c= unpadding_pkcs7('ICE ICE BABY\x05\x05\x05\x05')
	except ValueError:
		print("Bad Padding")
	try:
		c= unpadding_pkcs7('ICE ICE BABY\x01\x02\x03\x04')
	except ValueError:
		print("Bad Padding")

if __name__ == '__main__':
	main()

