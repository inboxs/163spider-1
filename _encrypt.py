import base64
from Crypto.Cipher import AES

param2='010001'
param3='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
param4='0CoJUm6Qyw8W8jud'

def get_params(page,param):
    # 获取encText,也就是params
    iv = "0102030405060708"
    key1 = param4
    key2 = "F" * 16
    encText = aes_encrypt(param,key1,iv)
    encText = aes_encrypt(encText.decode('utf-8'),key2,iv)
    return encText

def aes_encrypt(text,key,iv):
    count = 16 - len(text) % 16
    text = text + count * chr(count)
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encrypt_text = encryptor.encrypt(text.encode('utf-8'))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def get_encSecKey():
    key2 = "F" * 16
    encSEckey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSEckey

