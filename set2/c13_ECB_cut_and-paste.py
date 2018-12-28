from c10_Implement_CBC_mode import AES_ecb_encrypt, AES_ecb_decrypt, padding_pkcs7, unpadding_pkcs7
from Crypto.Cipher import AES
import os

KEY = os.urandom(16)

def encryption_oracle(plain):
	plain = padding_pkcs7(plain)
	return AES_ecb_encrypt(plain, KEY)
	
def decryption_oracle(cipher):
	plain = AES_ecb_decrypt(cipher, KEY)
	return unpadding_pkcs7(plain)

def profile_for(email):
	if "&" in email:
		email = email.split("&")[0]
	if "=" in email:
		email = email.split("=")[0]
	profile ={
		"email"	: email,
		"uid"	: "10",
		"role"	: "user"
	}
	return profile
	
def encode_profile(profile):
	enc_p  = "email=" + profile['email'] + "&"
	enc_p += "uid=" + profile['uid'] + "&"
	enc_p += "role=" + profile['role']
	return enc_p
	
def decode_profile(enc_profile):
	div_profile = enc_profile.split("&")
	profile = {}
	for property in div_profile:
		key , value = property.split("=")
		profile[key] = value
	return profile

if __name__ == '__main__':
	profile = profile_for("foo@bar.commm")
	profile = encode_profile(profile)
	enc_pro = encryption_oracle(profile)
	
	fake = profile_for("A"*10+"admin"+"\x0b"*11)
	fake = encode_profile(fake)
	enc_fake = encryption_oracle(fake)
	
	new_enc = enc_pro[:-16]+enc_fake[16:32]
	
	dec = decryption_oracle(new_enc)
	profile = decode_profile(dec)
	print(profile)
	

