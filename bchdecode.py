import bchlib
import hashlib
import os
import random

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) +7) // 8, byteorder='big')

# create a bch object
BCH_POLYNOMIAL = 137 #8219
BCH_BITS = 3 #16
bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

# random data
data = bytearray(os.urandom(512))

binary_data_pdf1= '1001001111001001110000000000000000000000001001011100000101100'
data = bytearray(bitstring_to_bytes(binary_data_pdf1))


# encode and make a "packet"
ecc = bch.encode(data)
packet = data + ecc

# print hash of packet
sha1_initial = hashlib.sha1(packet)
print('sha1: %s' % (sha1_initial.hexdigest(),))

def bitflip(packet):
    byte_num = random.randint(0, len(packet) - 1)
    bit_num = random.randint(0, 7)
    packet[byte_num] ^= (1 << bit_num)

# make BCH_BITS errors
for _ in range(BCH_BITS):
    bitflip(packet)

# print hash of packet
sha1_corrupt = hashlib.sha1(packet)
print('sha1: %s' % (sha1_corrupt.hexdigest(),))

# de-packetize
data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

# correct
bitflips = bch.decode_inplace(data, ecc)
print('bitflips: %d' % (bitflips))

# packetize
packet = data + ecc

# print hash of packet
sha1_corrected = hashlib.sha1(packet)
print('sha1: %s' % (sha1_corrected.hexdigest(),))

if sha1_initial.digest() == sha1_corrected.digest():
    print('Corrected!')
else:
    print('Failed')
