'''
Created on Dec 6, 2011

@author: akirk
'''

import codecs


def split_data(data, train=0.8):
    '''Splits data into train and test data.'''
    
    samples = len(data)
    divide = int(samples*train)
    
    return data[:divide], data[divide:]

if __name__ == '__main__': 
    
    TRANS = codecs.open("parole.transcription", "r", "iso8859_15").readlines()
    
    TRAIN_FILE = codecs.open("parole_train.transcription", "w", "iso8859_15")
    TEST_FILE = codecs.open("parole_test.transcription", "w", "iso8859_15")
    
    TRAIN, TEST = split_data(TRANS)
    
    for entry in TRAIN:
        TRAIN_FILE.write(entry)
    TRAIN_FILE.close()
    
    for entry in TEST:
        TEST_FILE.write(entry)
    TEST_FILE.close()