#! /usr/bin/env python

from random import randint
from Crypto.PublicKey import RSA


def generate_prime(bitsize=1024):
    RSAKey = RSA.generate(bitsize * 2)
    return RSAKey.key.p


class DiffieHellman:

    def __init__(self, p=None, g=None):
        if p is None:
            self.p = generate_prime()
            p = self.p
            self.g = randint(p / 2, p - 1)
        else:
            self.p = p
            self.g = g
        self.private_exponent = randint(p / 2, p - 1)

    def generate_public_broadcast(self):
        return self.p, self.g, pow(self.g, self.private_exponent, self.p)

    def get_shared_secret(self, public_share):
        return pow(public_share, self.private_exponent, self.p)

if __name__ == '__main__':
    personA = DiffieHellman()
    pA, gA, A = personA.generate_public_broadcast()
    print 'pA = %x' % pA
    print 'gA = %x' % gA
    print 'A = %x' % A

    personB = DiffieHellman(pA, gA)
    pB, gB, B = personB.generate_public_broadcast()
    print 'pB = %x' % pB
    print 'gB = %x' % gB
    print 'B = %x' % B
    assert(pA == pB)
    assert(gA == gB)

    sA = personA.get_shared_secret(B)
    sB = personB.get_shared_secret(A)
    print 'sA = %x' % sA
    print 'sB = %x' % sB
    assert(sA == sB)
