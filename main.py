import getopt
import sys

from datetime import datetime
from Bio.PDB import *
from Bio.PDB import MMCIF2Dict

def PDBtommCIF(infile, outfile, mode):
    parser = PDBParser()
    structure = parser.get_structure('', infile)

    if mode == "h":
        print("konwersja nagłówka")
        #TODO
    elif mode == "c":
        print("konwersja koordynatów")
        #TODO
    elif mode == "a":
        print("całość")
        #TODO

def mmCIFtoPDB(infile, outfile, mode):
    print("Conversion from mmCif to PDB")
    if mode == "h":
        print("konwersja nagłówka")
        mmcif_dict = MMCIF2Dict.MMCIF2Dict(infile)
        plik = open(outfile, 'w')
        # HEADER done
        if type(mmcif_dict['_database_PDB_rev.date_original']) is str:
            plik.writelines('{:10s}{:40s}{:12s}{:4s}\n'.format('HEADER',
                                                               mmcif_dict['_struct_keywords.pdbx_keywords'],
                                                               datetime.strptime(mmcif_dict['_database_PDB_rev.date_original'],"%Y-%m-%d").strftime("%d-%b-%y"),
                                                               mmcif_dict['_entry.id']))
        else:
            plik.writelines('{:10s}{:40s}{:12s}{:4s}\n'.format('HEADER',
                                                               mmcif_dict['_struct_keywords.pdbx_keywords'],
                                                               datetime.strptime(mmcif_dict['_database_PDB_rev.date_original'][0], "%Y-%m-%d").strftime("%d-%b-%y"),
                                                               mmcif_dict['_entry.id']))



        # OBSLTE

        # TITLE done
        tmp = ''
        cont = 1
        for i in mmcif_dict['_struct.title'].split(' '):
            if len(tmp + i + ' ') > 69:
                if cont == 1:
                    plik.writelines('{:10s}{:70s}\n'.format('TITLE', tmp))
                else:
                    plik.writelines('{:8s}{:>2s} {:69s}\n'.format('TITLE', str(cont), tmp))
                tmp = i + ' '
                cont += 1
            else:
                tmp += i + ' '
        if cont == 1:
            plik.writelines('{:10s}{:70s}\n'.format('TITLE', tmp))
        else:
            plik.writelines('{:8s}{:>2s} {:69s}\n'.format('TITLE', str(cont), tmp))
        # SPLIT

        # CAVEAT
            #plik.writelines('{:9s}{:2s}{:69s}\n'.format('TITLE', str(cont), tmp))

        # COMPND
        cont = 1
        if type(mmcif_dict['_entity.id']) is str:
            # MOL_ID
            if cont == 1:
                plik.writelines('{:18s}{:62s}\n'.format('COMPND    MOL_ID: ', mmcif_dict['_entity.id'] + ';'))
            else:
                plik.writelines(
                    '{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MOL_ID: ' + mmcif_dict['_entity.id'] + ';'))
            cont += 1
            # MOLECULE
            try:
                if mmcif_dict['_entity.pdbx_description'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
                                                                  'MOLECULE: ' + mmcif_dict['_entity.pdbx_description'] + ';'))
                    cont += 1
            except:
                print('No molecule')

            # CHAIN
            try:
                if mmcif_dict['_entity_poly.pdbx_strand_id'] != '?':
                    if i == 0:
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'CHAIN: ' + mmcif_dict[
                            '_entity_poly.pdbx_strand_id'].replace(',', ', ') + ';'))
                    cont += 1
            except:
                print('No chain')

            # FRAGMENT
            try:
                if mmcif_dict['_entity.pdbx_fragment'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
                                                                  'FRAGMENT: ' + mmcif_dict['_entity.pdbx_fragment'] + ';'))
                    cont += 1
            except:
                print('No fragment')

            # SYNONIM
            try:
                if mmcif_dict['_entity_name_com.name'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
                                                                  'SYNONIM: ' + mmcif_dict['_entity_name_com.name'] + ';'))
                    cont += 1
            except:
                print('No synonim')
            # EC
            try:
                if mmcif_dict['_entity.pdbx_ec'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
                                                                  'EC: ' + mmcif_dict['_entity.pdbx_ec'] + ';'))
                    cont += 1
            except:
                print('No EC')
            # ENGINEERED
            # TODO

            # MUTATION
            try:
                if mmcif_dict['_entity.pdbx_mutation'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MUTATION: YES;'))
                    cont += 1
            except:
                print('No EC')

            # OTHER_DETAILS
            try:
                if mmcif_dict['_entity.details'] != '?':
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
                                                                  'OTHER_DETAILS: ' + mmcif_dict['_entity.details'] + ';'))
                    cont += 1
            except:
                print('No OTHER_DETAILS')
        else:
            for i in range(0, len(mmcif_dict['_entity.id']), 1):
                # MOL_ID
                if cont == 1 :
                    plik.writelines('{:18s}{:62s}\n'.format('COMPND    MOL_ID: ', mmcif_dict['_entity.id'][i]+';'))
                else:
                    plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MOL_ID: '+ mmcif_dict['_entity.id'][i]+';'))
                cont += 1
                # MOLECULE
                try:
                    if mmcif_dict['_entity.pdbx_description'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MOLECULE: ' + mmcif_dict['_entity.pdbx_description'][i] + ';'))
                        cont += 1
                except:
                    print('No molecule')

                # CHAIN
                try:
                    if mmcif_dict['_entity_poly.pdbx_strand_id'][i] != '?':
                        if i == 0:
                            plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'CHAIN: ' + mmcif_dict['_entity_poly.pdbx_strand_id'].replace(',',', ') + ';'))
                        cont += 1
                except:
                    print('No chain')

                # FRAGMENT
                try:
                    if mmcif_dict['_entity.pdbx_fragment'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'FRAGMENT: ' + mmcif_dict['_entity.pdbx_fragment'][i] + ';'))
                        cont += 1
                except:
                    print('No fragment')

                # SYNONIM
                try:
                    if mmcif_dict['_entity_name_com.name'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'SYNONIM: ' + mmcif_dict['_entity_name_com.name'][i] + ';'))
                        cont += 1
                except:
                    print('No synonim')
                # EC
                try:
                    if mmcif_dict['_entity.pdbx_ec'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'EC: '+ mmcif_dict['_entity.pdbx_ec'][i]+';'))
                        cont += 1
                except:
                    print('No EC')
                # ENGINEERED
                #TODO

                # MUTATION
                try:
                    if mmcif_dict['_entity.pdbx_mutation'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MUTATION: YES;'))
                        cont += 1
                except:
                    print('No EC')

                # OTHER_DETAILS
                try:
                    if mmcif_dict['_entity.details'][i] != '?':
                        plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'OTHER_DETAILS: ' + mmcif_dict['_entity.details'][i] + ';'))
                        cont += 1
                except:
                    print('No OTHER_DETAILS')
        # SOURCE
        tmp = mmcif_dict['_entity_src_nat.entity_id']
        if type(mmcif_dict['_entity_src_nat.entity_id']) is str:
            # MOL_ID
            if cont == 1:
                plik.writelines('{:18s}{:62s}\n'.format('SOURCE    MOL_ID: ', mmcif_dict['_entity_src_nat.entity_id'] + ';'))
            else:
                plik.writelines(
                    '{:7s} {:>2s} {:72}\n'.format('SOURCE', str(cont), 'MOL_ID: ' + mmcif_dict['_entity_src_nat.entity_id'] + ';'))
            cont += 1
        #     # MOLECULE
        #     try:
        #         if mmcif_dict['_entity.pdbx_description'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
        #                                                           'MOLECULE: ' + mmcif_dict['_entity.pdbx_description'][
        #                                                               i] + ';'))
        #             cont += 1
        #     except:
        #         print('No molecule')
        #
        #     # CHAIN
        #     try:
        #         if mmcif_dict['_entity_poly.pdbx_strand_id'][i] != '?':
        #             if i == 0:
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'CHAIN: ' + mmcif_dict[
        #                     '_entity_poly.pdbx_strand_id'].replace(',', ', ') + ';'))
        #             cont += 1
        #     except:
        #         print('No chain')
        #
        #     # FRAGMENT
        #     try:
        #         if mmcif_dict['_entity.pdbx_fragment'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
        #                                                           'FRAGMENT: ' + mmcif_dict['_entity.pdbx_fragment'][
        #                                                               i] + ';'))
        #             cont += 1
        #     except:
        #         print('No fragment')
        #
        #     # SYNONIM
        #     try:
        #         if mmcif_dict['_entity_name_com.name'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
        #                                                           'SYNONIM: ' + mmcif_dict['_entity_name_com.name'][
        #                                                               i] + ';'))
        #             cont += 1
        #     except:
        #         print('No synonim')
        #     # EC
        #     try:
        #         if mmcif_dict['_entity.pdbx_ec'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
        #                                                           'EC: ' + mmcif_dict['_entity.pdbx_ec'][i] + ';'))
        #             cont += 1
        #     except:
        #         print('No EC')
        #     # ENGINEERED
        #     # TODO
        #
        #     # MUTATION
        #     try:
        #         if mmcif_dict['_entity.pdbx_mutation'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MUTATION: YES;'))
        #             cont += 1
        #     except:
        #         print('No EC')
        #
        #     # OTHER_DETAILS
        #     try:
        #         if mmcif_dict['_entity.details'][i] != '?':
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont),
        #                                                           'OTHER_DETAILS: ' + mmcif_dict['_entity.details'][
        #                                                               i] + ';'))
        #             cont += 1
        #     except:
        #         print('No OTHER_DETAILS')
        # else:
        #     for i in range(0, len(mmcif_dict['_entity.id']), 1):
        #         # MOL_ID
        #         if cont == 1 :
        #             plik.writelines('{:18s}{:62s}\n'.format('COMPND    MOL_ID: ', mmcif_dict['_entity.id'][i]+';'))
        #         else:
        #             plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MOL_ID: '+ mmcif_dict['_entity.id'][i]+';'))
        #         cont += 1
        #         # MOLECULE
        #         try:
        #             if mmcif_dict['_entity.pdbx_description'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MOLECULE: ' + mmcif_dict['_entity.pdbx_description'][i] + ';'))
        #                 cont += 1
        #         except:
        #             print('No molecule')
        #
        #         # CHAIN
        #         try:
        #             if mmcif_dict['_entity_poly.pdbx_strand_id'][i] != '?':
        #                 if i == 0:
        #                     plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'CHAIN: ' + mmcif_dict['_entity_poly.pdbx_strand_id'].replace(',',', ') + ';'))
        #                 cont += 1
        #         except:
        #             print('No chain')
        #
        #         # FRAGMENT
        #         try:
        #             if mmcif_dict['_entity.pdbx_fragment'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'FRAGMENT: ' + mmcif_dict['_entity.pdbx_fragment'][i] + ';'))
        #                 cont += 1
        #         except:
        #             print('No fragment')
        #
        #         # SYNONIM
        #         try:
        #             if mmcif_dict['_entity_name_com.name'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'SYNONIM: ' + mmcif_dict['_entity_name_com.name'][i] + ';'))
        #                 cont += 1
        #         except:
        #             print('No synonim')
        #         # EC
        #         try:
        #             if mmcif_dict['_entity.pdbx_ec'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'EC: '+ mmcif_dict['_entity.pdbx_ec'][i]+';'))
        #                 cont += 1
        #         except:
        #             print('No EC')
        #         # ENGINEERED
        #         #TODO
        #
        #         # MUTATION
        #         try:
        #             if mmcif_dict['_entity.pdbx_mutation'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'MUTATION: YES;'))
        #                 cont += 1
        #         except:
        #             print('No EC')
        #
        #         # OTHER_DETAILS
        #         try:
        #             if mmcif_dict['_entity.details'][i] != '?':
        #                 plik.writelines('{:7s} {:>2s} {:72}\n'.format('COMPND', str(cont), 'OTHER_DETAILS: ' + mmcif_dict['_entity.details'][i] + ';'))
        #                 cont += 1
        #         except:
        #             print('No OTHER_DETAILS')
        # KEYWDS
        tmp = ''
        cont = 1
        for i in mmcif_dict['_struct_keywords.text'].split(','):
            if len(tmp+','+i) > 68:
                if cont == 1:
                    plik.writelines('{:10s}{:70s}\n'.format('KEYWDS', tmp))
                else:
                    plik.writelines('{:8s}{:>2s}{:69s}\n'.format('KEYWDS', str(cont), tmp))
                tmp = i+','
                cont +=1
            else:
                tmp += i+','
        if cont == 1:
            plik.writelines('{:10s}{:70s}\n'.format('KEYWDS', tmp))
        else:
            plik.writelines('{:8s}{:>2s}{:69s}\n'.format('KEYWDS', str(cont), tmp))
        # EXPDTA
        # TODO continuation
        plik.writelines('{:10s}{:70s}\n'.format('EXPDTA', mmcif_dict['_exptl.method']))

        # MDLTYP
        # TODO continuation
        plik.writelines('{:10s}{:70s}\n'.format('MDLTYP', mmcif_dict['_struct.pdbx_model_type_details']))

        # AUTHOR
        tmp = ''
        cont = 1
        for i in mmcif_dict['_audit_author.name']:
            tmp2 = i.split(', ')
            name = ''
            if len(tmp2) < 2:
                name = tmp2[0]
            else:
                name = tmp2[1]+tmp2[0]
            if len(tmp + name + ',') > 68:
                if cont == 1:
                    plik.writelines('{:10s}{:70s}\n'.format('AUTHOR', tmp))
                else:
                    plik.writelines('{:8s}{:>2s}{:69s}\n'.format('AUTHOR', str(cont), tmp))
                tmp = name + ','
                cont += 1
            else:
                tmp += name + ','
        if cont == 1:
            plik.writelines('{:10s}{:70s}\n'.format('AUTHOR', tmp))
        else:
            plik.writelines('{:8s}{:>2s}{:69s}\n'.format('AUTHOR', str(cont), tmp))

        # REVDAT
        #TODO Modification detail
        if type(mmcif_dict['_database_PDB_rev.date_original']) is str:
            plik.writelines('{:8s}{:>2s}{:3s}{:10s}{:8s}{:1s}'.format('REVDAT',
                                                                      mmcif_dict['_database_PDB_rev.num'],
                                                                      ' ',
                                                                      datetime.strptime(mmcif_dict['_database_PDB_rev.date'],"%Y-%m-%d").strftime("%d-%b-%y"),
                                                                      mmcif_dict['_database_PDB_rev.replaces'],
                                                                      mmcif_dict['_database_PDB_rev.mod_type']))
        else:
            for i in range(len(mmcif_dict['_database_PDB_rev.num'])-1, -1, -1):
                plik.writelines('{:8s}{:>2s}{:3s}{:10s}{:8s}{:1s}'.format('REVDAT',
                                                                      mmcif_dict['_database_PDB_rev.num'][i],
                                                                      ' ',
                                                                      datetime.strptime(mmcif_dict['_database_PDB_rev.date'][i], "%Y-%m-%d").strftime("%d-%b-%y"),
                                                                      mmcif_dict['_database_PDB_rev.replaces'][i],
                                                                      mmcif_dict['_database_PDB_rev.mod_type'][i] ))


        # SPRSDE

        # JRNL

        # REMARK 3 - Refinement

        # REMARK 200 - X - ray Diffraction Data Collection

        # REMARK 210 - NMR Data Collection

        # REMARK 230 - Neutron Diffraction Data Collection

        # REMARK 240 - Electron Crystallography Data Collection

        # REMARK 245 - EM Data Collection

        # REMARK 265 - Solution Scattering Data Collection

        # REMARK 280 - Crystallization

        # REMARK 800 - Site Details

        plik.close()

    elif mode == "c":
        print("konwersja koordynatów")
        parser = MMCIFParser()
        structure = parser.get_structure('', infile)
        io = PDBIO()
        io.set_structure(structure)
        io.save(outfile)
    elif mode == "a":
        print("całość")
        #TODO

def usage():
    print("usage: main [-h] [-i inputfilename] [-o outputfilename] [-c convType] [-m mode]")
    print("   -h                displays this help message")
    print("   -i inputfilename  sets the input file as inputfilename can be all dir")
    print("   -o outputfilename sets the output file as outputfilename can be all dir")
    print("   -c convType       sets the conversion type as convType")
    print("                     convType = PDB - conversion from PDB format to mmCIF")
    print("                     convType = mmCIF - conversion from mmCIF format to PDB")
    print("   -m mode           sets the mode of conversion as mode")
    print("             default mode = a - conversion all file")
    print("                     mode = h - conversion header only")
    print("                     mode = c - conversion coordinates only")



def main(argv):
    inputFile = ''
    outputFile = ''
    conversionType = ''
    mode = 'a'
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:m:",["--help","--ifile=","--ofile=","--convType=", "--mode="])
    except getopt.GetoptError as err:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
           outputFile = arg
        elif opt in ("-c", "--convType"):
            conversionType = arg
        elif opt in ("-m", "--mode"):
            mode = arg
            if mode not in ('a', 'h', 'c'):
                print("error: wrong mode argument")
                usage()
                sys.exit(2)
        else:
            print("error: unrecognized parameter")
            usage()
            sys.exit(2)

    if conversionType == 'PDB':
        PDBtommCIF(inputFile,outputFile,mode)
    elif conversionType == 'mmCIF':
        mmCIFtoPDB(inputFile,outputFile,mode)
    else:
        print("error: conversion Type not recognized or not set")
        usage()
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
