from decodefunctions import getFiveCharChecksum
import zlib
from random import randint

if __name__ == "__main__":

    hexchars='ABCDEF0123456789'
    #print(zlib.crc32('ADCE02A8FC4106D'))
    #print(hex(zlib.crc32('A7947889C7B80000E000001')))
    randhexdic={}
    checksumdic={}
    randchar=3
    testpersample=1000
    limittest=1000
    writefile= open('fgbhexcollisions.txt',"w")
    infile=open('fgbuser.txt',"r")


    c='ACCE09A52C41C0D'
    print(getFiveCharChecksum(c))
    j=0
    collisions=0
    for rh in infile:
        realhex=rh.strip()

        if len(realhex)==15 and j<limittest:
            j+=1

            if j%1000==0:
                print(j)
            realchecksum = getFiveCharChecksum(realhex)


            randomhex = []
            collision = []
            i=0
            while i < testpersample:

                randposlist=[]

                while len(randposlist) < randchar :
                    randpos = randint(0, 14)
                    if randpos not in randposlist:
                        randposlist.append(randpos)

                newhex=realhex
                for randpos2 in randposlist:
                    hexchar = hexrandom = realhex[randpos2]

                    while hexchar==hexrandom:
                        hexrandom = hexchars[(randint(0,15))]


                    if randpos2 == 0:
                        newhex = hexrandom + newhex[1:]
                    elif randpos2 == 14:
                        newhex = newhex[:-1] + hexrandom
                    else:
                        newhex = newhex[0:randpos2] + hexrandom + newhex[randpos2+1:]
                    #print(randpos)

                randomhex.append(newhex)

                if realchecksum ==getFiveCharChecksum(newhex):
                    collision.append((newhex,realhex))
                    writefile.write(':'.join(( '\n\nActual    ',    realhex, realchecksum,   '\nCollision ', newhex , getFiveCharChecksum(newhex)        )))
                    collisions+=1
                    print( newhex,getFiveCharChecksum(newhex),realhex,realchecksum)
                i += 1
                #print(getFiveCharChecksum(newhex))

                #print(realhex,len(realhex))
                #checksumdic[checksum] = hex




    #print(i)
    #print(len(checksumdic),i,(i-len(checksumdic))/float(i))
    print(j)
    writefile.write('\n\nUnique FGB tested: '+str(j)+ '  Collisions: '+ str(collisions)+'    Randomize Char : '+str(randchar)+'     Test per sample: ' + str(testpersample))
    infile.close()
    writefile.close()
    '''
    for i in range(10):
        randomhex = ''
        for d in range(15):
            randomhex=randomhex+hexchars[(randint(0,16))]
        #checksumdic[str(zlib.crc32(randomhex))]=randomhex
        checksumdic[str(getFiveCharChecksum(randomhex))] = randomhex
    print(len(checksumdic))
    '''