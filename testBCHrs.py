import unireedsolomon as rs
import decodefunctions as Fcn
import Gen2functions as Sgb
import bch1correct

b = '0000000011100110000010001111010011001001100001100001100101100001100010001010000001000111110000000000000000000000000000000000000000000000000011111111111111000000000100000000110000011010000000001001011000'
print('hi',len(b))
byte_string=bch1correct.bitstring_to_bytes(b)
# print(byte_string,len(byte_string))
#
# print(len(b), Fcn.bin2hex(b))
#
# print(Fcn.bin2dec(b[:16]))
calcbch = Sgb.calcBCH(b, 0, 202, 250)
comp_b =  '00'+ b + calcbch
print(comp_b,len(comp_b))
hex=Fcn.bin2hex(comp_b)
print(hex)
print(len(hex))

print('------')
print(byte_string,len(byte_string))
print('------')
coder2 = rs.RSCoder(32,26,3)
encode2 =coder2.encode(byte_string,True)
print(encode2)
print(repr(encode2))
print(type(encode2))
print(len(encode2))
decode2=coder2.decode(encode2)
print(decode2)
#print(len(decode2)[0])
print(type(decode2))
print('corrected: ', decode2[0])
print(len(decode2[0]))
print(len(byte_string))
print(len(decode2[1]))

print('----')
ecc=decode2[1]
print(ecc)
print('ECC: ', bytes(repr(ecc),encoding='utf-8'))
ecc_array=bytearray(repr(ecc),encoding='utf-8')
print(len(ecc_array),ecc_array)
print('----')
eccreduild=''
for e in ecc_array:
    eccreduild=eccreduild+Fcn.dec2bin(repr(e))
    print(e,repr(e),type(e),Fcn.dec2bin(repr(e)))
print(eccreduild,len(eccreduild))
bchsgb=bch1correct.bitstring_to_bytes(calcbch)
print(calcbch)
