'''
Created on Oct 27, 2011

@author: akirk
'''

import os
from subprocess import Popen

def wav_convert(cwd):
    '''Converts existing .wav files to 16kHz, 16 bit, mono audio files for 
    training with sphinx.'''

    files = os.listdir(cwd)

    prefix = "new_files/"
    os.mkdir(prefix)

    sox_cmd = ["sox", "", "-r", "16k", "-b", "16", "-c", "1", "", "mixer", "-l"]

    for filename in files:
        new_file = prefix + filename
        sox_cmd[1] = filename
        sox_cmd[-3] = new_file
        sox = Popen(sox_cmd)
        sox.communicate()
    
if __name__ == '__main__':
    
    wav_convert(os.getcwd())