#! /usr/bin/env python

from random import randint
from Crypto.Cipher import AES
from binascii import a2b_hex


def gen_rand_data(length=16):
    return ''.join(chr(randint(0, 255)) for i in range(length))


def pkcs_7_pad(data, final_len=None):
    if final_len == None:
        final_len = (len(data) / 16 + 1) * 16
    padding_len = final_len - len(data)
    return data + chr(padding_len) * padding_len


class PaddingException(Exception):

    """ Padding for input data incorrect """


def pkcs_7_unpad(data):
    padding_len = ord(data[len(data) - 1])
    if padding_len > 16:  # Block size
        raise PaddingException
    if padding_len == 0:
        raise PaddingException
    for i in range(len(data) - padding_len, len(data)):
        if ord(data[i]) != padding_len:
            raise PaddingException
    return data[:-padding_len]


def AES_128_ECB_encrypt(data, key, pad=False):
    cipher = AES.new(key, AES.MODE_ECB)
    if pad:
        data = pkcs_7_pad(data)
    return cipher.encrypt(data)


def AES_128_ECB_decrypt(data, key, unpad=False):
    cipher = AES.new(key, AES.MODE_ECB)
    decr = cipher.decrypt(data)
    if unpad:
        decr = pkcs_7_unpad(decr)
    return decr


def xor_data(A, B):
    return ''.join(chr(ord(A[i]) ^ ord(B[i])) for i in range(len(A)))


def AES_128_CBC_encrypt(data, key, iv):
    data = pkcs_7_pad(data)
    block_count = len(data) / 16
    encrypted_data = ''
    prev_block = iv
    for b in range(block_count):
        cur_block = data[b * 16:(b + 1) * 16]
        encrypted_block = AES_128_ECB_encrypt(
            xor_data(cur_block, prev_block), key)
        encrypted_data += encrypted_block
        prev_block = encrypted_block
    return encrypted_data


def AES_128_CBC_decrypt(data, key, iv):
    block_count = len(data) / 16
    decrypted_data = ''
    prev_block = iv
    for b in range(block_count):
        cur_block = data[b * 16:(b + 1) * 16]
        decrypted_block = AES_128_ECB_decrypt(cur_block, key)
        decrypted_data += xor_data(decrypted_block, prev_block)
        prev_block = cur_block
    return pkcs_7_unpad(decrypted_data)


AES_key = None
AES_iv = None


def init(key):
    from Crypto.Hash import SHA256
    global AES_key
    str_key = str(key)
    h = SHA256.new()
    h.update(str(key))
    long_key = a2b_hex(h.hexdigest())
    AES_key = long_key[:16]
    AES_iv = long_key[16:]


def encrypt(data):
    return AES_128_CBC_encrypt(data, AES_key, AES_iv)


def decrypt(data):
    return AES_128_CBC_decrypt(data, AES_key, AES_iv)

if __name__ == '__main__':
    text = 'abcdefghijklmnopqrstuvwxyz!'
    key = 'abcdef1234567890'

    init(key)
    assert(decrypt(encrypt(text)) == text)
    print "[+] CBC decrypt(encrypt(text))==text test passed"
