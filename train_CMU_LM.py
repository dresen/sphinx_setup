'''
Created on Dec 6, 2011

@author: akirk
'''

import subprocess, codecs

def train_lm(filename):
    '''Trains a LM using CMULMTK. $filename is the relative path to the input
    file.'''
    
    name = filename.split(".")[0]
    
    log = name + ".lm.log"
    logfile = codecs.open(log, "w", "iso8859_15")
    
    #Create vocabulary file
    vocab = name + ".vocab"
    subprocess.call("text2wfreq < %s | wfreq2vocab > %s" % (filename, vocab), 
                    shell=True, stderr=logfile)
    
    #Create idngram file
    idngram = name + ".idngram"
    cmd = "text2idngram -vocab %s -idngram %s < %s" % (vocab, idngram, filename)
    subprocess.call(cmd, shell=True, stderr=logfile)
    
    #Create ARPA format language model
    arpa = name + ".arpa"
    cmd = "idngram2lm -vocab_type 0 -idngram %s -vocab %s -arpa %s" % (idngram,
                                                                      vocab,
                                                                      arpa)
    subprocess.call(cmd, shell=True, stderr=logfile)
    
    #Create binary DMP file
    binary = name + ".lm.DMP"
    cmd = "sphinx_lm_convert -i %s -o %s" % (arpa, binary)
    subprocess.call(cmd, shell=True, stderr=logfile)
    

if __name__ == '__main__':
    
    train_lm("parole.lm.input")