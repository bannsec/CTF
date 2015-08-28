#!/usr/bin/python3

from sys import argv
import os
import argparse

def auto_int(x):
        try:
                return int(x)
        except:
                return int(x,16)

parser = argparse.ArgumentParser(description='Create private RSA key from primes. Export in PEM format.')
parser.add_argument('p', metavar='p', type=auto_int, nargs=1,
                   help='First RSA Prime')
parser.add_argument('q', metavar='q', type=auto_int, nargs=1,
                   help='Second RSA Prime')
parser.add_argument('e', metavar='e', type=auto_int, nargs='?', default=65537,
                   help='Optional: Public Exponent (Default: 65537)')

args = parser.parse_args()


##########################
# http://crypto.stackexchange.com/questions/25498/how-to-create-a-pem-file-for-storing-an-rsa-key
import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

def pempriv(n, e, d, p, q, dP, dQ, qInv):
    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()
    for x in [0, n, e, d, p, q, dP, dQ, qInv]:
        seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodestring(der).decode('ascii'))


# http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


p = args.p[0]
q = args.q[0]
e = args.e
n = p * q
phi = (p - 1) * (q - 1)
d = modinv(e,phi) 
dP = d % (p-1)
dQ = d % (q-1)
qInv = modinv(q,p)

privKey = pempriv(n,e,d,p,q,dP,dQ,qInv)

print(privKey)
