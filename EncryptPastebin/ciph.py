#!/usr/bin/env python3

import json
import codecs
import binascii

def postCt2cipher_text(postCt):
    postCt = postCt.replace('~', '=').replace('!', '/').replace('-', '+')
    cipher_text = codecs.decode(bytes(postCt, 'utf8'), 'base64')
    return cipher_text

def cipher_text2postCt(cipher_text):
    postCt = codecs.encode(cipher_text, 'base64')
    postCt = postCt.decode('utf8')
    postCt = postCt.replace('=', '~').replace('/', '!').replace('+', '-').replace('\n', '')
    return postCt

def switchBS(bs):
    """
    Switch bytes and string.
    """
    if type(bs) == type(b''):
        return "".join(map(chr, bs))
    return n2s(int(''.join( hex(ord(c))[2:].rjust(2,'0') for c in bs),16))

def s2hex(s):
    if type(s) == str :
        s = switchBS(s) 
    return binascii.hexlify(s)

def xor_string(s1,s2):
    """
    Exclusive OR (XOR) @s1, @s2 byte by byte
    return the xor result with minimun length of s1,s2
    """
    if type(s1) != type(s2) :
        raise TypeError('Input must be the same type, both str or bytes.')
    if type(s1) == type(s2) == bytes :
        return b''.join([byte(a^b) for a,b in zip(s1,s2)])
    return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)])

def CBC_XOR(cipher, origin, to) :
    """   
    Give : 
        @cipher : CBC cipher 
        @origin : origin plaintext
        @to     : fake plaintext
    """
    if len(cipher)%8 == 0 :
        raise Exception('Error block size')
        
    if not len(cipher) == len(origin) == len(to):
        raise Exception('cipher, origin plaintext, fake plaintext must be the same length.')

    return xor_string(xor_string(cipher,origin), to)

postCt = 'dOBSRluUlvf9XOPN!p3EHqsQrH5kvgM5kuklldYmB!AKYLbby5wLN7esnqvKeuWyrWdGn6vh90GDPpw1wTLjxwSvJESUE-NNyy7!Daa60JsE67OmDja3yTPlG8TleoIhfTEbEpsRMOP0pZ94Xwa4HeY8Iz2L5aMtFZFZrLAEUEYJohNYE0v22s39ShLYB5l0AK9ppmZl4O5waw8RZo1ZfA~~'
# plain_text = '{"flag": "^FLAG^09c843db81f89a10c00376e486d2976a04797bdd579dd47ee6e75fc8e156f81d$FLAG$", "id": "1", "key": "yVOtRKvqPvdxlYtrecJJcw~~"}'
fake_text = '{"id":"1"}'

plain_text_hex = binascii.hexlify(bytes(plain_text, 'utf8'))
fake_text_hex = binascii.hexlify(bytes(fake_text, 'utf8'))
cipher_text = postCt2cipher_text(postCt)
cipher_text_hex = binascii.hexlify(cipher_text)

print('cipher_text_hex: {}\n'.format(cipher_text_hex))
print('plain_text_hex: {}\n'.format(plain_text_hex))
print('fake_text_hex: {}\n'.format(fake_text_hex))

def PKCS7padding(hex_text):
    pad = int((32-len(hex_text)%32)/2)
    for i in range(pad):
        p = "%0.2x" % pad
        hex_text += bytes(p, 'utf8')
    return hex_text

plain_text_hex_padded = PKCS7padding(plain_text_hex)
print('plain_text_hex_padded: {}\n'.format(plain_text_hex_padded))

PT = plain_text_hex_padded[-32:]
IV = cipher_text_hex[-64:-32]
FT = PKCS7padding(fake_text_hex)

print('PT: {}'.format(PT))
print('IV: {}'.format(IV))
print('FT: {}'.format(FT))

# X = PT ^ IV
X = list(hex(int(chr(a), 16) ^ int(chr(b), 16)) for a, b in zip(PT, IV))
X = ''.join(list(map(lambda x:str(x)[-1], X)))
print('X: {}'.format(X))

# newIV = X ^ FT 
newIV = list(hex(int(a, 16) ^ int(chr(b), 16)) for a, b in zip(X, FT))
newIV = ''.join(list(map(lambda x:str(x)[-1], newIV)))
print('newIV: {}'.format(newIV))

fake_post_hex = bytes(newIV, 'utf8') + cipher_text_hex[-32:]
print('fake_post: {}'.format(fake_post_hex))
fake_post = binascii.unhexlify(fake_post_hex)
fake_postCt = cipher_text2postCt(fake_post)
print('fake_postCt: {}'.format(fake_postCt))
