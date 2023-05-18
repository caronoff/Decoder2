def process_file(file_path, decode_path):
    f = open(file_path)
    with open(decode_path, 'a') as nf:
        for line in f.readlines():
            nf.writelines(line)
    f.close()
    nf.close()


if __name__ == "__main__" :
    process_file('uin.csv','uincopy.csv')
