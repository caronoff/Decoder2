import bchlib
import hashlib
import os
import random
import Gen2functions as Sgb
import decodefunctions as Fcn
import bch1correct

def is_prime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                #print(num, "is not a prime number")
                #print(i, "times", num // i, "is", num)
                return False
                break
        else:
            return True

    # if input number is less than
    # or equal to 1, it is not prime
    else:
        return False

def bitflip(packet,byte_num):
    #byte_num = random.randint(0, len(packet) - 1)
    bit_num = random.randint(0, 7)
    packet[byte_num] ^= (1 << bit_num)

# create a bch object
BCH_POLYNOMIAL = 8219
BCH_BITS = 6

primes=[]
for i in range(8500):
    if is_prime(i):
        primes.append(i)



f=open('bchtext.txt','w')

for p in primes:
    try:
        f.write('\n====' + str(p) + '=====')
        bch = bchlib.BCH(p, BCH_BITS)



        b='0000000011100110000010001111010011001001100001100001100101100001100010001010000001000111110000000000000000000000000000000000000000000000000011111111111111000000000100000000110000011010000000001001011000'
        print(len(b),Fcn.bin2hex(b))

        print(Fcn.bin2dec(b[:16]))
        calcbch = Sgb.calcBCH(b, 0, 202, 250)
        comp_b=  b+calcbch
        print('5 0 in front',len(comp_b))
        #comp_b='0'*5+comp_b


        # make complete with bch
        data=bytearray(bch1correct.bitstring_to_bytes(comp_b))






        packet = data
        print('Total Packet size',len(packet))

        # print hash of packet
        sha1_initial = hashlib.sha1(packet)
        print('sha1: %s' % (sha1_initial.hexdigest(),))
        f.write('\nsha1: %s' % (sha1_initial.hexdigest(),))


        ecc = bch.encode(packet)

        # de-packetize
        data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

        print('ecc calc',len(ecc), bch.ecc_bytes,bch.ecc_bits)
        print('data len',len(data))



        # Random scramble BCH_BITS errors
        for i in range(BCH_BITS):
            bitflip(packet,i+3)


        # print hash of packet
        sha1_corrupt = hashlib.sha1(packet)

        print('sha1: %s' % (sha1_corrupt.hexdigest(),))
        f.write('\nsha1 corrupt: %s' % (sha1_corrupt.hexdigest(),))

        # de-packetize
        #data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

        # correct
        bitflips = bch.decode_inplace(data, ecc)
        print('bitflips: %d' % (bitflips))

        f.write('\nECC bits: {}'.format(bch.ecc_bits))
        f.write('\nECC bits: {}'.format(bch1correct.byte_to_binary(ecc)))
        f.write('\nBCH bits: {}'.format(calcbch))

        f.write('\nbitflips: %d' % (bitflips))
        # packetize
        packet = data + ecc

        # print hash of packet
        sha1_corrected = hashlib.sha1(packet)
        print('sha1: %s' % (sha1_corrected.hexdigest(),))
        f.write('\nsha1 corrected: %s' % (sha1_corrected.hexdigest(),))
        if sha1_initial.digest() == sha1_corrected.digest():
            print('Corrected!')
            f.write('\nCorrected!')
            f.write('\n'+bch1correct.byte_to_binary(data))
            f.write('\n' + b)
        else:
            print('Failed')
            f.write('\nFailed')
    except :
        f.write('\n'+str(p) +' is bad parameter')



f.close()
