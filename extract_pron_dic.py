# -*- coding: iso-8859-15 -*-
'''
Created on Nov 30, 2011

@author: akirk
'''

import codecs

MIRROR = "mirror"

def easy_sort(freq_list):
    '''Returns a dictionary where the key is a word and the value is the 
    first occurring transcription of that word in freq_list. Supposing that the
    first transcription is empty, a subsequent transcription is chosen.'''
    dic = {}
    for entry in freq_list:
        if dic.has_key(entry[0]):
            if dic[entry[0]] == "":  # If the transcription is in later entry
                dic[entry[0]] = entry[2]
            else:
                pass
        else:
            dic[entry[0]] = entry[2]
    return dic


def mirror(freq_list):
    '''Returns a dictionary where the key is a word and the value is the 
    first occurring transcription of that word in freq_list.'''
    dic = {}
    checklist = {u'å': u'aa', u'ø':"oe", u'æ':"ae", u'ö':"oe", u'ä':"ae",
                  u'ž':"z1", u'-':"dash", u'é':"e"}
    ignore = [u'_', u"'", u'0', u'']
    for entry in freq_list:
        elem = ""
        for char in entry[0]:
            if char in checklist.keys():
                char = checklist[char]
            elif char in ignore:
                continue
            elem += char + " "
        elem = elem.strip() 

        if dic.has_key(entry[0]):
            pass
        else:
            dic[entry[0]] = elem
    return dic


def multiple_sort(freq_list):
    '''Returns a dictionary where each pronunciation form has a different
    surface form.'''
    dic = {}
    for entry in freq_list:
        if dic.has_key(entry[0]):
            dic[entry[0]].append(entry[2])
        else:
            dic[entry[0]] = [entry[2]]
    return dic    
    
    
def freq_sort(freq_list, mode):
    '''Easy: Assumes the most frequent transcription is the first entry and 
    creates a dictionary with words as key and transcriptions as values.'''
    
    if mode == "assume_first":
        dic = easy_sort(freq_list)
    elif mode == "multiple":
        dic = multiple_sort(freq_list)
    elif mode == MIRROR:
        dic = mirror(freq_list)
    else:
        pass
    return dic


def sphinx_format(sampa):
    '''Converts Parole SAMPA to a format usable by sphinxtrain. Removes
    diacritics for stress and stoed and converts uppercase characters to
    double lowercase.'''
    
    diacritics = [#"1",
                 #"2",
                 #"3",
                 #"!",
                 #":",
                 #"-"
                 ]
    stressmarkers = ["1", "2", "3"]
    sphinx = ""
    prev = ""
    for char in sampa:
        if char in diacritics:
            continue
        else:
            
            # Normalisation
            if char.isupper() == True:
                char = "%s(2)" % char.lower()
                sphinx += char + " "
                prev = char
            
            # diacritics appended to subsequent phone  
            elif char in stressmarkers:
                sphinx += char
                
            # diacritics appended to previous phone
            elif char == "!":
                sphinx = sphinx[:-1] + "! "
            elif char == ":":
                sphinx = sphinx[:-1] + prev + " "
                
            # assimilated schwa
            elif char == "-":
                sphinx += "dash" + " "            
                
            # Base case
            else:
                sphinx += char + " "
                prev = char
    return sphinx.strip()
      

def extract_dic(freqs, delimit, mode="assume_first", trainer="sphinx", 
                fin=True):
    '''Extracts entries from a frequency list created with 
    extract_freq_list.py where the delimiter is usually "|||". '''
    
    if fin:
        entries = []
        for line in freqs:
            entry = line.split(delimit)
            entry = [en.strip() for en in entry]
            if entry[-1].strip() == "":
                continue
            else:
                entries.append(entry)
    else:
        entries = freqs
    
    dic = freq_sort(entries, mode=mode)
    
    
    if trainer == "sphinx" and mode != MIRROR:
        for key in dic.keys():
            dic[key] = sphinx_format(dic[key])
                
    return dic



if __name__ == '__main__':
    
    FREQS = codecs.open("parole_pronun.freq", "r", "iso8859_15").readlines()
    DELIMIT = "|||"
    DIC = extract_dic(FREQS, DELIMIT)
    DIC_FILE = codecs.open("parole.dic", "w", "iso8859_15")
    
    for element in DIC:
        DIC_FILE.write("%s\t%s\n" % (element, DIC[element]))
    DIC_FILE.close()