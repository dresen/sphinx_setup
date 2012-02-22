# -*- coding: iso-8859-15 -*-
'''
Created on Dec 6, 2011

@author: akirk

Does not handle audio files!

'''

import os, sys, codecs
from extract_freq_list import extract_freq_list 
from extract_pron_dic import extract_dic
from phone_from_dic import extract_phones
from extract_transcription import extract_transcription
from split_data import split_data
from train_CMU_LM import train_lm


ETC = "etc"
WAV = "wav"


def manage_setup(path, create):    
    '''Setup database structure (folders) and change to top directory'''
    if os.path.isdir(path):
        if len(os.listdir(path)) == 0:
            pass
        else:
            if create:
                sys.exit("Sphinx DB exists.")
            else:
                pass
    else:
        os.mkdir(path)
        
    os.chdir(path)
    
    if create:
        os.mkdir(ETC)
        os.mkdir(WAV)
        print "DB structure created"


def compute_freqs(griddir, name):
    '''Compute pronunciation frequencies''' 
    freqs = extract_freq_list(griddir)
    freqfile = codecs.open("%s/%s_pronun.freq" % (ETC, name), "w", ENC)
    for entry in freqs:
        freqfile.write("%s ||| %s ||| %s\n" % (entry[0], entry[1], entry[2]))
    freqfile.close()
    
    print "Pronunciation frequencies computed"

    return freqs
    

def create_dic(freqlist, name):    
    '''Create pronunciation dictionary based on pronunciation frequencies'''
    delimit = "|||"
    dic = extract_dic(freqlist, delimit, fin=False, mode=DIC_CONF)
    dic_file = codecs.open("%s/%s.dic" % (ETC, name), "w", ENC)
    for element in dic:
        dic_file.write("%s\t%s\n" % (element, dic[element]))
    dic_file.close()
    
    print "Pronunciation dictionary created"

    return dic


def create_phonelist(dic, name):
    '''Extract phones from the pronunciation dictionary'''
    phones = extract_phones(dic, fin=False)
    phonefile = codecs.open("%s/%s.phone" % (ETC, name), "w", ENC)
    for element in phones:
        phonefile.write(element + "\n")
    phonefile.close()
    
    print "Phones extracted from pronunciation dictionary"
    

def extract_orthography(name, griddir, lm_name):
    '''Create transcription file and language model data'''
    
    trans = extract_transcription(griddir)
    trans.sort(key=lambda pair: pair[1])
    transcription = codecs.open("%s/%s.transcription" % (ETC, name), 
                                "w", ENC)
    langmodel = codecs.open(lm_name, "w", ENC)    
    for entry in trans:
        langmodel.write("<s> %s </s>\n" % entry[0])
    trans = ["<s> %s </s> (%s)\n" % (entry[0], entry[1]) 
             for entry in trans]
    transcription.writelines(trans)
    langmodel.close()
    transcription.close()
    
    print "Transcription file and language model input file created"

    return trans

def split_orthography(trans, name):    
    '''Split transcription into train and test data'''
    train, test = split_data(trans)
    trainfile = codecs.open("%s/%s_train.transcription"  % (ETC, name), 
                             "w", ENC)
    testfile = codecs.open("%s/%s_test.transcription"  % (ETC, name), 
                            "w", ENC)
    for entry in train:
        trainfile.write(entry)
    trainfile.close()
    
    for entry in test:
        testfile.write(entry)
    testfile.close()
    
    print "Data segmented into training and test data"



def setup_db(path, griddir, create=True):
    '''Sets up the db used to train sphinx. Does not move audio files due to 
    corpus size and number of speakers.'''    
    
    name = path.rsplit("/")[-1]
    
    
    lm_name = "%s/%s.lm.input"  % (ETC, name)
    
    #Create folders
    manage_setup(path, create)
    
    #Create word distribution list
    freqs = compute_freqs(griddir, name)

    #Create pronunciation dictionary file
    dic = create_dic(freqs, name)
    
    #Create phone list from dictionary list
    create_phonelist(dic, name)
    
    #Create LM training data
    trans = extract_orthography(name, griddir, lm_name)
    
    #Create training and test data for Sphinx
    split_orthography(trans, name)
        
    #Train language model
    train_lm(lm_name)
    
    print "Training language model"
    
    
    print "Successfully set up training database in %s!\n" % path
    print "You should now move your audio files to the wav/ folder and subsequently call create_fileids.py."
    print "Remember to distribute the audio files according to speaker."
    print "(And remember the fillers!)"
    
    
if __name__ == '__main__':
    
    
    
    DBNAME = sys.argv[1] #"/home/akirk/Desktop/article"
    GRIDDIR = sys.argv[2] #"/home/akirk/Desktop/CMOL/Corpus/"
    ENC = "iso8859_15"
    DIC_CONF = sys.argv[3] #"assume_first" # assume_first or multiple
    #$create: True for new DB and False for update
    setup_db(DBNAME, GRIDDIR, create=True)