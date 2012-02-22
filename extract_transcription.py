# -*- coding: iso-8859-15 -*-
'''
Created on Dec 6, 2011

@author: akirk

Must set LM variable!

'''

import codecs, os
from Interval import merge_intervals
from extract_freq_list import create_interval


def extract_transcription(griddir, mode="Text"):
    '''Extracts orthographic transcription from praat textgrids. Can also 
    create training data for CMULMTK.'''
    gridlist = os.listdir(griddir)
    transcriptions = []
    for filename in gridlist:
        grid = codecs.open(griddir + "/" + filename, 
                           "r", "iso8859_15").readlines()
        text_intervals = []
        if mode == "Text":
            terminate = "item [2]" 
        else:
            terminate = False
        for lineno, line in enumerate(grid):
            if terminate in line:
                break
            if "intervals " in line:
                #print line 
                interval = create_interval(line, lineno, grid, mode)
                text_intervals.append(interval)
        
        orthography = reduce(merge_intervals, text_intervals)
        transcriptions.append((orthography.surf, filename.split(".")[0]))
    return transcriptions

if __name__ == '__main__':
    
    GRIDDIR = "/home/akirk/Desktop/CMOL/Corpus/" 
    LM = True
    MODE = "text"
    
    if not LM:
        TRANSCRIPTION = codecs.open("parole.transcription", "w", "iso8859_15")
    else:
        TRANSCRIPTION = codecs.open("parole.lm.input", "w", "iso8859_15")
        
    TRANS = extract_transcription(GRIDDIR, mode=MODE)
    
    if LM:
        for entry in TRANS:
            TRANSCRIPTION.write("<s> %s </s>\n" % entry[0])
    else:
        for entry in TRANS:
            TRANSCRIPTION.write("<s> %s </s> (%s)\n" % (entry[0], entry[1]))
    TRANSCRIPTION.close()