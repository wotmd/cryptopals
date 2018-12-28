from c10_Implement_CBC_mode import *
from Crypto.Cipher import AES
import os

KEY = os.urandom(16)
IV = os.urandom(16)

def CreateParam(userdata):
	userdata = userdata.replace(';', '').replace('=', '')
	parameter  = "comment1=cooking%20MCs;userdata="
	parameter += userdata
	parameter += ";comment2=%20like%20a%20pound%20of%20bacon"
	return parameter

def encrypParam(Param):
	plain = padding_pkcs7(Param)
	return AES_cbc_encrypt(plain, KEY, IV)
	
def decryptParam_CheckAdmin(EncParam):
	DecParam = AES_cbc_decrypt(EncParam, KEY, IV)
	Param = unpadding_pkcs7(DecParam)
	print(Param)
	return (";admin=true;" in Param)

def CreateParam(userdata):
	userdata = userdata.replace(';', '').replace('=', '')
	parameter  = "comment1=cooking%20MCs;userdata="
	parameter += userdata
	parameter += ";comment2=%20like%20a%20pound%20of%20bacon"
	return parameter	

def BitFlipping(data,idx):
	return data[:idx]+chr(ord(data[idx])^1)+data[idx+1:]
	
	
if __name__ == '__main__':
	param = CreateParam("X"*16+":admin<true:") ## ':' = 90 , ';' = 91   /  '<'=92, '=' = 93
	enc = encrypParam(param)
	enc = BitFlipping(enc, 32)
	enc = BitFlipping(enc, 38)
	enc = BitFlipping(enc, 43)
	if decryptParam_CheckAdmin(enc):
		print("Admin!!")


