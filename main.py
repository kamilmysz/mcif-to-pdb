import getopt
import sys
import requests
import os
import re
from bs4 import BeautifulSoup

def convert (infile , outfile, log):
    print("Uploading file to serwer...")
    conversionUrl = 'http://mmcif.pdbj.org/converter/index.php'
    downloadUrl = "http://mmcif.pdbj.org/converter/download.php"
    logUrl ='http://mmcif.pdbj.org/converter/data/'
    payload = {'l': 'en', 'm': 'c'}
    session = requests.session()
    files = {'src': open(os.path.realpath(infile), 'r')}
    r = session.post(conversionUrl, data=payload, files = files)
    if r.ok:
        if not 'Please upload a file again.'.encode('utf-8') in r.content:
            parsed_html = BeautifulSoup(r.content, "html.parser")
            payload = {e['name']: e.get('value', '') for e in parsed_html.find_all('input', {'name': True})}
            payload['l']= 'en'
            r = session.post(conversionUrl, data=payload) #rozpoczecie konwersji
            if r.ok:
                print("Conversion in progress...")
                parsed_html = BeautifulSoup(r.content, "html.parser")
                while r.ok and 'Check the conversion progress'.encode('utf-8') in r.content:
                    payload = {e['name']: e.get('value', '') for e in parsed_html.find_all('input', {'name': True})}
                    payload['l']= 'en'
                    r = session.post(conversionUrl, data=payload)
                    parsed_html = BeautifulSoup(r.content, "html.parser")
                #pobieranie pliku i zapis
                if r.ok:
                    print("Downloading file...")
                    payload = {e['name']: e.get('value', '') for e in parsed_html.find_all('input', {'name': True})}
                    payload['l'] = 'en'
                    if log:
                        r = session.get(logUrl+payload['p']+"/maxit.log")
                        if r.ok:
                            if  os.path.isfile('conversion.log'):
                                with open('conversion.log', 'ab') as f:
                                    for chunk in r.iter_content(1024):
                                        f.write(chunk)
                            else:
                                with open('conversion.log', 'wb') as f:
                                    for chunk in r.iter_content(1024):
                                        f.write(chunk)
                    r = session.post(downloadUrl, data=payload)
                    if r.ok:
                        with open(outfile, 'wb') as f:
                            for chunk in r.iter_content(1024):
                                f.write(chunk)
                        print("Succeeded.")
                    else:
                        print("Error: onection issue please try again.")
                        sys.exit(4)
                else:
                    print("Error: Conection issue please try again.")
                    sys.exit(4)
            else:
                print("Error: Conection issue please try again.")
                sys.exit(4)
        else:
            print("Error: File format not recognized.")
            sys.exit(4)
    else:
        print("Error: Conection issue please try again.")
        sys.exit(4)


def cutPDBFile(infile, outfile, mode, chain):
    ifile = open(infile, 'r')
    ofile = open(outfile, 'w')
    if mode == "h":
            for line in ifile.readlines():
                if (line.startswith('HEADER') or line.startswith('OBSLTE') or line.startswith('TITLE') or line.startswith('SPLIT') or line.startswith('CAVEAT') or line.startswith('COMPND')
                    or line.startswith('SOURCE') or line.startswith('KEYWDS') or line.startswith('EXPDTA') or line.startswith('NUMMDL') or line.startswith('MDLTYP')
                    or line.startswith('AUTHOR') or line.startswith('REVDAT') or line.startswith('SPRSDE') or line.startswith('JRNL') or line.startswith('REMARK') or line.startswith('END')):
                    ofile.write(line)
    elif mode == "c":
        chainsInFile = []
        if chain == 'all':
            with open(infile, 'r') as f:
                for line in f.readlines():
                    if (line.startswith('HEADER') or line.startswith('DBREF') or line.startswith('SEQADV') or line.startswith('SEQRES') or line.startswith('MODRES')
                        or line.startswith('HET') or line.startswith('HETNAM') or line.startswith('HETSYN') or line.startswith('FORMUL') or line.startswith('HELIX')
                        or line.startswith('SHEET') or line.startswith('SSBOND') or line.startswith('LINK') or line.startswith('CISPEP') or line.startswith('SITE')
                        or line.startswith('CRYST') or line.startswith('ORIGX') or line.startswith('SCALE') or line.startswith('MTRIX') #dalej koordynaty
                        or line.startswith('MODEL') or line.startswith('ATOM') or line.startswith('ANISOU') or line.startswith('TER') or line.startswith('HETATM')
                        or line.startswith('ENDMDL') or line.startswith('CONECT') or line.startswith('MASTER') or line.startswith('END')):
                        ofile.write(line)
        else:
            chains = chain.split(',')
            with open(infile, 'r') as f:
                for line in f:
                    if 'COMPND' in line and 'CHAIN' in line:
                        chainsInFile += (re.sub(r'(COMPND.+CHAIN:|;|\s)','', line.rstrip()).split(','))
            for chain in chains:
                if chain not in chainsInFile:
                    print('Error: Chosen chain : '+chain+' not found in file')
                    sys.exit(3)
            with open(infile, 'r') as f:
                for line in f.readlines():
                    if (line.startswith('HEADER') or (line.startswith('DBREF') and line[12] in chains) or (line.startswith('SEQADV') and line[16] in chains) or (line.startswith('SEQRES') and line[11] in chains)
                        or (line.startswith('MODRES') and line[16] in chains) or (line.startswith('HET') and line[12] in chains) or line.startswith('HETNAM') or line.startswith('HETSYN') or line.startswith('FORMUL')
                        or (line.startswith('HELIX') and line[19] in chains) or (line.startswith('SHEET') and line[21] in chains) or (line.startswith('SSBOND') and line[15] in chains and line[29] in chains)
                        or (line.startswith('LINK') and line[21] in chains and line[51] in chains) or (line.startswith('CISPEP')and line[15] in chains and line[29] in chains)
                        or (line.startswith('SITE') and line[22] in chains and line[33] in chains and line[44] in chains and line[55] in chains)
                        or line.startswith('CRYST') or line.startswith('ORIGX') or line.startswith('SCALE') or line.startswith('MTRIX') #dalej same koordynaty
                        or line.startswith('MODEL') or (line.startswith('ATOM') and line[21] in chains) or (line.startswith('ANISOU') and line[21] in chains)
                        or (line.startswith('TER') and line[21] in chains) or (line.startswith('HETATM') and line[21] in chains)
                        or line.startswith('ENDMDL') or line.startswith('CONECT') or line.startswith('MASTER') or line.startswith('END')):
                            ofile.write(line)
    ifile.close()
    ofile.close()




def fileConversion(infile, outfile, mode, log, chain):
    print("Input file name: " + os.path.realpath(infile))
    print("Output file name: " + os.path.realpath(outfile))
    sys.stdout.write("Chosen mode: ")
    if mode == "h":
        print("Header Conversion")
        with open(infile, 'r') as f:
            first_line = f.readline()
        if 'HEADER' in first_line: #pdb
            cutPDBFile(infile, infile+'tmp', mode, chain)
            convert(infile+'tmp', outfile, log)
            os.remove(infile+'tmp')
        elif 'data' in first_line: #mmcif
            convert(infile, outfile+'tmp', log)
            cutPDBFile(outfile+'tmp', outfile, mode, chain)
            os.remove(outfile+'tmp')
        else:
            print("Error: File format not recognized.")
            sys.exit(3)

    elif mode == "c":
        print("Coordinates Conversion")
        with open(infile, 'r') as f:
            first_line = f.readline()
        if 'HEADER' in first_line: #pdb
            cutPDBFile(infile, infile+'tmp', mode, chain)
            convert(infile+'tmp', outfile, log)
            os.remove(infile+'tmp')

        elif 'data' in first_line: #mmcif
            convert(infile, outfile+'tmp', log)
            cutPDBFile(outfile+'tmp', outfile, mode, chain)
            os.remove(outfile+'tmp')
        else:
            print("Error: File format not recognized.")
            sys.exit(3)

    elif mode == "a":
        print("All File Conversion")
        convert(infile, outfile, log)

def usage():
    print()
    print("Usage: main [-h] [-l] -i inputfilename -o outputfilename [-m mode]")
    print("            [-c chain1,chain2,...]")
    print("   -h                displays this help message")
    print("   -l                with this parametr log file will be created")
    print("   -i inputfilename  sets the input file as inputfilename can be all dir")
    print("   -o outputfilename sets the output file as outputfilename can be all dir")
    print("   -m mode           sets the mode of conversion as mode")
    print("             default mode = a - all file")
    print("                     mode = h - header only")
    print("                     mode = c - coordinates only")
    print("  -c chains     only with -m c alows selection of chains to convert")
    print()
    print("Examples:")
    print(" main -i 1asy.pdb -o 1asy.cif - coversion of all 1asy.pdb to 1asy.cif")
    print(" main -l -i 1asy.pdb -o 1asy.cif -m h - coversion of headers from 1asy.pdb to 1asy.cif with log")
    print(" main -i 1asy.pdb -o 1asy.cif -m c -c A,B - coversion of coordinates from chains A and B of 1asy.pdb to 1asy.cif")



def main(argv):
    inputFile = ''
    outputFile = ''
    mode = 'a'
    chain = 'all'
    log = False;
    try:
        opts, args = getopt.getopt(argv,"hli:o:m:c:",["--help","--log","--ifile=","--ofile=", "--mode=", "--chain="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-l", "--log"):
            log = True
        elif opt in ("-i", "--ifile"):
            if os.path.isfile(arg):
                inputFile = arg
            else:
                print("Error: input file not found")
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            if not os.path.isfile(arg):
                outputFile = arg
            else:
                print("Error: output file allready exists")
                sys.exit(2)
        elif opt in ("-m", "--mode"):
            mode = arg
            if mode not in ('a', 'h', 'c'):
                print("Error: wrong mode argument")
                usage()
                sys.exit(2)
        elif opt in ("-c", "--chain"):
            if mode != 'c':
                print("Error: for chain selection mode must be coordinates only (-m c)")
                usage()
                sys.exit(2)
            else:
                chain = arg
        else:
            print("Error: unrecognized parameter")
            usage()
            sys.exit(2)
    if inputFile == '' or outputFile == '':
        print("Error: input file parameter and output flie parameter must be specified")
        usage()
        sys.exit(2)

    fileConversion(inputFile,outputFile,mode,log,chain)

if __name__ == "__main__":
   main(sys.argv[1:])