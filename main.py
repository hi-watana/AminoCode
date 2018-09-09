from urllib import request
import gzip
import sys

URL = 'ftp://ftp.wwpdb.org/pub/pdb/data/monomers/components.cif.gz'

#PREFIX_DATA = 'data'
#PREFIX_ID = '_chem_comp.id'
PREFIX_ONE_LETTER = '_chem_comp.one_letter_code'
PREFIX_THREE_LETTER = '_chem_comp.three_letter_code'

constant_values = [
        #PREFIX_DATA,
        #PREFIX_ID,
        PREFIX_ONE_LETTER,
        PREFIX_THREE_LETTER,
        ]

constants_length_map = {c: len(c) for c in constant_values}

BLOCK_SIZE = len(constant_values)
DICT_NAME = 'AMINO_CODE_TABLE'

if __name__ == '__main__':
    with request.urlopen(URL) as g:
        with gzip.open(g, mode='r') as f:
            necessary_lines = filter(
                    lambda l: any(
                        l[:length] == v for (
                            v, length) in constants_length_map.items()),
                    (b.decode() for b in f))

            print('%s = {' % DICT_NAME)
            for line1 in necessary_lines:
                line1 = line1.split()[1]
                line2 = next(necessary_lines).split()[1]
                if line1 == '?' or len(line1) != 1 or len(line2) != 3:
                    continue
                print('\t\'%s\' : \'%s\',' % (line2, line1))
            print('}')
