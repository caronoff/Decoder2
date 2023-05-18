import decodehex2
def uin_decode(inputfile,outputfile):

    hexcodes = open(inputfile)
    decoded = open(outputfile, 'w')



    i = 0
    decoded.write("""Input Message,Message Type,15 Hex ID,Protocol Type,Beacon Type,TAC,Country Code,Country Name,Message protocol,Encoded Pos,Fixed Bits,Errors\n""")

    for line in hexcodes.readlines():
        i += 1
        #print i, count, i/float(count),i/float(count)*100

        line = str(line.strip())
        decoded.write('{h},'.format(h=str(line)))
        try:
            c = decodehex2.Beacon(str(line))
            if c.gentype=='first' :
                c = decodehex2.BeaconFGB(str(line))



                decoded.write('{},'.format(c.getmtype()))


                decoded.write('{},'.format(c.hexuin()))

                decoded.write('{},'.format(c.protocolflag()))

                decoded.write('{},'.format(c.btype()))

                decoded.write('{},'.format(c.gettac()))
                decoded.write('{},'.format(c.get_mid()))
                decoded.write('{},'.format(c.get_country()))
                decoded.write('{},'.format(c.loctype()))
                decoded.write('{},'.format(c.getencpos()))

                decoded.write('{},'.format(c.fbits()))
                errors='None'
                if len(c.errors)>0:
                    errors = ' : '.join(c.errors)
                decoded.write('{},'.format(errors))
            else:
                decoded.write('Not an FGB long message')


        except decodehex2.HexError as e:

            decoded.write(e.value)




        decoded.write('\n')

    decoded.close()

if __name__ == "__main__":
    uin_decode('uin.csv','uin_out.csv')
