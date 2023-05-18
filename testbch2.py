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


#primes=[8219]
f=open('bchtext.txt','w')
for p in primes:
    try:
        f.write('\n===='+str(p)+'=====')
        bch = bchlib.BCH(p, BCH_BITS)
        recompose=''
        # sample hex 00E608F4C986196188A047C000000000000FFFC0100C1A00960
        print(p)

        b='0000000011100110000010001111010011001001100001100001100101100001100010001010000001000111110000000000000000000000000000000000000000000000000011111111111111000000000100000000110000011010000000001001011000'
        print(len(b),Fcn.bin2hex(b))
        print(Fcn.bin2hex(b))
        print(Fcn.bin2dec(b[:16]))
        calcbch = Sgb.calcBCH(b, 0, 202, 250)
        comp_b= b+calcbch

        comp_b='0'*5+comp_b
        print(len(comp_b))

        # make complete with bch
        data=bytearray(bch1correct.bitstring_to_bytes(comp_b))
        #print(len(data))
        recompose = ''
        for e in data:
            c = Fcn.dec2bin(e).zfill(8)
            # print(e, c)
            recompose = recompose + c
        #print(len(recompose))

        newdata=bytearray(recompose)
        print('match',data==newdata)
        f.write('\nmatch: {} len: {} '.format(str(data==newdata),len(recompose)))




        packet = data
        ecc = bch.encode(packet)


        print('ecc calc',len(ecc))

        # print hash of packet
        sha1_initial = hashlib.sha1(packet)
        print('sha1: %s' % (sha1_initial.hexdigest(),))
        f.write('\nsha1: %s' % (sha1_initial.hexdigest(),))

        # make BCH_BITS errors
        for i in range(BCH_BITS-1):
            bitflip(packet,i+2)

        bitflip(packet,25)
        # print hash of packet
        sha1_corrupt = hashlib.sha1(packet)

        print('sha1: %s' % (sha1_corrupt.hexdigest(),))
        f.write('\nsha1 corrupt: %s' % (sha1_corrupt.hexdigest(),))
        # de-packetize
        f.write('\nECC bits: {}'.format(bch.ecc_bits))

        data, ecc =  packet[:-len(calcbch_array)], packet[-len(calcbch_array):]#data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

        # correct
        bitflips = bch.decode_inplace(data, ecc)
        print('\nbitflips: %d' % (bitflips))
        f.write('\nbitflips: %d' % (bitflips))
        # packetize
        packet = data + ecc

        # print hash of packet
        sha1_corrected = hashlib.sha1(packet)
        print('sha1: %s' % (sha1_corrected.hexdigest(),))
        f.write('\nsha1: %s' % (sha1_corrected.hexdigest(),))
        if sha1_initial.digest() == sha1_corrected.digest():
            print('Corrected!')
            f.write('\nCorrected!')
        else:
            print('Failed')
            f.write('\nFailed')
    except:
        f.write('Parameter Failed')

f.close()
