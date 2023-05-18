import bchlib
import hashlib
import os
import random
import Gen2functions as Sgb
import decodefunctions as Fcn
import bch1correct
from bitstring import BitArray
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


#print(primes)
f=open('bchtext.txt','w')
for p in primes:
    try:
        f.write('\n===='+str(p)+'=====')
        bch = bchlib.BCH(p, BCH_BITS,reverse=False)
        recompose=''
        # random data
        while recompose=='' or '1'  in recompose[:6] :
            recompose = ''
            data = bytearray(os.urandom(26))    #was 26
            for e in data:
                c=Fcn.dec2bin(e).zfill(8)
                #print(e, c)
                recompose=recompose+c

        #print(bch1correct.byte_to_binary(data),len(bch1correct.byte_to_binary(data)))
        print(recompose[6:],len(recompose[6:]))
        newdata=bytearray(bch1correct.bitstring_to_bytes('00'+recompose[6:]))
        #newdata=BitArray('0b'+recompose[6:])
        print(newdata)
        print('match',data==newdata)

        f.write('\nmatch: {} len: {}  {} '.format(str(data == newdata), len(recompose[6:]),recompose[6:]))

        # encode and make a "packet"
        ecc = bch.encode(newdata)    #data

        recompose_ecc='' #Fcn.dec2bin(ecc[0])''

        for e in ecc:
            c=Fcn.dec2bin(e).zfill(8)
            #print(e, c)
            recompose_ecc=recompose_ecc+c
        f.write('\nECC recompose: {}  Length: {} len ecc: {}'.format(recompose_ecc,len(recompose_ecc),len(ecc)))

        # recompose_ecc2 = ''
        #
        # for e in ecc:
        #     c = Fcn.dec2bin(e) #.zfill(8)
        #     # print(e, c)
        #     recompose_ecc2 = recompose_ecc2 + c
        # f.write('\nECC recompose: {}  Length: {}'.format(recompose_ecc2, len(recompose_ecc2)))


        #newecc=bytearray(bch1correct.bitstring_to_bytes(recompose_ecc))
        #print('match ecc',ecc==newecc)
        print(recompose_ecc)
        #print(Sgb.calcBCH(recompose,0,202,250))   #was recompose[6:]
        #f.write(recompose_ecc)
        calcbch=Sgb.calcBCH(recompose[6:],0,202,250) #was recompose[6:]
        f.write('\nBCH caclulated: {}  Length: {}'.format(calcbch,len(calcbch)))
        packet = data + ecc
        print(len(ecc))
        # print hash of packet
        sha1_initial = hashlib.sha1(packet)
        print('sha1: %s' % (sha1_initial.hexdigest(),))
        f.write('\nsha1: %s' % (sha1_initial.hexdigest(),))

        # make BCH_BITS errors
        for i in range(BCH_BITS-1):
            bitflip(packet,i+2)

        bitflip(packet,20)
        # print hash of packet
        sha1_corrupt = hashlib.sha1(packet)

        print('sha1: %s' % (sha1_corrupt.hexdigest(),))
        f.write('\nsha1 corrupt: %s' % (sha1_corrupt.hexdigest(),))
        # de-packetize
        f.write('\nECC bits: {} bytes: {} '.format(bch.ecc_bits,bch.ecc_bytes))
        data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:] # data, ecc = packet[:-len(ecc)], packet[-len(ecc):] #
        f.write('\nECC bits: {} bytes: {} '.format(bch.ecc_bits, bch.ecc_bytes))
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
            f.write('\n'+str(len(data))+str(len(ecc))+str(type(data)))
            f.write('\n'+str(len(packet)))

        else:
            print('Failed')
            f.write('\nFailed')
    except:
        f.write('Parameter Failed')

f.close()
