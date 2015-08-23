#!/usr/bin/python3

from fractions import gcd
import itertools
import binascii

e = 65537

f = open("primesList","r")

pubKey = 0xc20a1d8b3903e1864d14a4d1f32ce57e4665fc5683960d2f7c0f30d5d247f5fa264fa66b49e801943ab68be3d9a4b393ae22963888bf145f07101616e62e0db2b04644524516c966d8923acf12af049a1d9d6fe3e786763613ee9b8f541291dcf8f0ac9dccc5d47565ef332d466bc80dc5763f1b1139f14d3c0bae072725815f

encData = 0x49f573321bdb3ad0a78f0e0c7cd4f4aa2a6d5911c90540ddbbaf067c6aabaccde78c8ff70c5a4abe7d4efa19074a5249b2e6525a0168c0c49535bc993efb7e2c221f4f349a014477d4134f03413fd7241303e634499313034dbb4ac96606faed5de01e784f2706e85bf3e814f5f88027b8aeccf18c928821c9d2d830b5050a1e

# The following functions are from: http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
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

comp = f.readlines()

# Sanitize input
comp2 = [int(x[:-1],16) for x in comp]

print("Shaking primes free")

primes = set([])
numPrimes = 0

for pair in itertools.combinations(comp2,2):
	# Don't care if they're the same
	if pair[0] == pair[1]:
		continue
	
	d = gcd(pair[0],pair[1])
	
	# Check for legit win
	if d != 1:
		primes = set(list(primes) + [d])
		if len(primes) > numPrimes:
			numPrimes = len(primes)
			print("Recovered {0}/30 primes".format(numPrimes))
			if numPrimes == 30:
				print("Recovered All Primes")
				break

print("Recovering possible decryption keys")

phi = 0

# Get p,q pairs
for p,q in itertools.combinations(primes,2):
	# Check if we're working with the right primes
	if p * q == pubKey:
		print("Matched pubKey:\np = {0}\nq = {1}".format(p,q))
		phi = (p-1) * (q-1)
		break

# Check that we found correct primes
if phi == 0:
	print("Error: We didn't find the two primes...")
	exit(0)

# Calc the key
privKey = modinv(e,phi)

print("Recovered private key: {0}".format(privKey))

# Decrypt it
decrypted = pow(encData,privKey,pubKey)

# Decode it
decoded = binascii.unhexlify(hex(decrypted)[2:])

print("Recovered message: {0}".format(decoded))

f.close()
