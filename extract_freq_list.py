'''
Created on Nov 1, 2011

@author: akirk
'''

import codecs, os
from Interval import Interval



def create_transcription(intervals): 
    '''Creates a string representation of the transcriptions in Intervals.
    '''
    transcription = ""
    for obj in intervals:
        transcription += obj.surf  
    return transcription.strip()


def compile_list(alignments):
    '''Creates a list of dictionary entries from the aligned Interval objects.
    '''
    dic = []
    for alignment in alignments:
        dic.append((alignment[0].surf, create_transcription(alignment[1])))
    return dic
        
        
def align_intervals(text, sampa):
    '''Aligns Interval objects based on time codes. Intervals are
    in chronological order. 1 Text Interval <= 1 SAMPA Interval(s)'''
    
    out = []
    for int_t in text:
        aligned = []
        align = False
        if int_t.surf == "":
            continue
        for int_s in sampa:
            if int_t.xmin == int_s.xmin:
                aligned.append(int_s)
                if int_t.xmax == int_s.xmax:
                    pass
                else:   
                    align = True
            elif int_t.xmax != int_s.xmax and align == True:
                aligned.append(int_s)
            elif int_t.xmax == int_s.xmax:
                aligned.append(int_s)
                align = False
            else:
                pass
        out.append((int_t, aligned))
        
    return out

          
def count_freq(entry_list):
    '''Counts the frequency of the transcriptions of the words in the data.'''
        
    dic = {}
    for pair in entry_list:
        if dic.has_key(pair):
            dic[pair] += 1
        else:
            dic[pair] = 1 
    return dic


def sort_entries(dic):
    '''Sorts entries based on raw frequency.'''
    
    outlist = []
    for key in dic.keys():
        outlist.append((key[0], dic[key], key[1]))
    outlist.sort(reverse=True)
    return(outlist)
                
def create_interval(line, num, grid, mode):
    '''Creates an interval from the input'''
    return Interval(
                line.split("[")[-1].split("]")[0], # num
                mode, 
                float(grid[num+1].split()[-1]), # xmin
                float(grid[num+2].split()[-1]), # xmax
                grid[num+3].split()[-1].strip("\"") # surf
                    )
    

def extract_freq_list(griddir):
    '''Extracts a pronunciation dictionary from the Parole corpus with multiple
    transcriptions for each orthographic entry.'''
    
    gridlist = os.listdir(griddir)
    grid_dic = []
    for filename in gridlist:
        grid = codecs.open(griddir + "/" + filename, 
                           "r", "iso8859_15").readlines()
        text_intervals = []
        sampa_intervals = []
        mode = "Text"
        for lineno, line in enumerate(grid):
            if "item [2]" in line:
                mode = "Transcription"
            if "intervals " in line:
                interval = create_interval(line, lineno, grid, mode)
                if mode == "Text":
                    text_intervals.append(interval)
                else:
                    sampa_intervals.append(interval)
        
        if sampa_intervals == []:
            alignment = [(x.surf, "") for x in text_intervals]
        else:
            alignment = align_intervals(text_intervals, sampa_intervals)
            grid_dic.extend(compile_list(alignment))
    dictionary = count_freq(grid_dic)
    freq_list = sort_entries(dictionary)
                    
    return freq_list


if __name__ == '__main__':
    
    GRIDDIR = "/home/akirk/Desktop/CMOL/Corpus/" 
    
    FREQ_FILE = codecs.open("parole_pronun.freq", "w", "iso8859_15")
    
    FREQS = extract_freq_list(GRIDDIR)
    
    for entry in FREQS:
        FREQ_FILE.write("%s ||| %s ||| %s\n" % (entry[0], entry[1], entry[2]))
    FREQ_FILE.close()