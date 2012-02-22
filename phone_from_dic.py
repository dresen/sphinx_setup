'''
Created on Nov 30, 2011

@author: akirk
'''

import codecs
from extract_freq_list import count_freq


def extract_phones(dic, fin=True, withfreq=False):
    '''Extracts the number of phones in a pronunciation dictionary. Optionally
    with frequencies and defaults to file intput'''
    
    temp = []
    if fin:
        for line in dic:
            trans = line.strip().split("\t")[1]
            temp.extend(trans.split())   
    else:
        for entry in dic.values():
            temp.extend(entry.split())
    phones = count_freq(temp)
    if withfreq:
        output = ["%s\t%s" % (key, phones[key]) for key in phones.keys()] 
    else:
        output = phones.keys()
    output.append("SIL")
    return output


if __name__ == '__main__':
    
    DIC = codecs.open("parole.dic", "r", "iso8859_15").readlines()
    PHONE = extract_phones(DIC)
    PHONE_FILE = codecs.open("parole.phone", "w", "iso8859_15")
    
    for element in PHONE:
        PHONE_FILE.write(element + "\n")
    PHONE_FILE.close()