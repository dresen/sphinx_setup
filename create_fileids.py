'''
Must be deployed in top folder of the training database
Audio files must be distributed manually

Currently works for 1 speaker

'''

ENC = "iso8859_15"

import codecs, os, sys

def listdir(path):
    '''Checks whether a folder exists and returns an error message when it 
    fails.'''
    if not os.path.isdir(path):
        sys.exit("No %s folder." % path)
    else:
        return os.listdir(path)    


def load_transcript_ids(transcript):
    '''Returns a list of file identifiers'''
    
    return [x.rsplit("(", 1)[-1].strip()[:-1] for x in transcript]


def output_files(train, test, name):
    '''Writes the file ids to their respective files, ready for training'''
    
    test_ids_file = codecs.open("etc/%s_test.fileids" % name, 
                                "w", ENC)
    train_ids_file = codecs.open("etc/%s_train.fileids" % name, 
                                 "w", ENC)
    
    test_ids_file.writelines(test)
    test_ids_file.close()
    train_ids_file.writelines(train)
    train_ids_file.close()

def loadfiles(etc):
    '''Loads the transcript files where the necessary file ids are stored'''
    
    transcript_train = False
    transcript_test = False
    
    for filename in etc:
        if "_test.transcription" in filename:
            transcript_test = codecs.open("etc/%s" % filename, 
                                     "r", ENC).readlines()
        if "_train.transcription" in filename:
            transcript_train = codecs.open("etc/%s" % filename, 
                                     "r", ENC).readlines()
    if not transcript_test or not transcript_train:
        sys.exit("Missing training or test transcription files.")
    else:
        testfile = load_transcript_ids(transcript_test)
        trainfile = load_transcript_ids(transcript_train)
        
    return (testfile, trainfile)


def create_fileids(cwd, name):
    '''Creates two "fileids" files for training and testing. The files are 
    divided according to the transcription files.'''
        
    os.chdir(cwd)
    test_ids = []
    train_ids = []
    path = ""

    etclist = listdir("etc/")
    trainfile, testfile = loadfiles(etclist)
    
    wavpath = "wav/"    
    
    speakers = listdir(wavpath)
    for speaker in speakers:
        wavdir = wavpath + speaker
        wavlist = [x.rsplit('.', 1)[0] for x in os.listdir(wavdir)]   
        
        for uid in trainfile:
            if uid in wavlist:
                train_ids.append("%s/%s\n" % (speaker, uid))
            else:
                print uid
        for uid in testfile:
            if uid in wavlist:
                test_ids.append("%s/%s\n" % (speaker, uid))
            else:
                pass
    train_ids.sort()
    test_ids.sort()
    
    output_files(train_ids, test_ids, name)
    
    return train_ids, test_ids

if __name__ == '__main__':
    

    
    DIR = sys.argv[1]
    NAME = DIR.strip("/").rsplit("/", 1)[-1]
    TRAIN, TEST = create_fileids(DIR, NAME)
