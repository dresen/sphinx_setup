'''
Created on Nov 30, 2011

@author: akirk
'''

class Interval(object):
    '''Class for intervals in PRAAT TextGrids.'''
    
    def __init__(self, n_id, mode, xmin, xmax, surface):
        '''Information needed to align transcription and text intervals from
        TextGrids.'''
        self.uid = n_id
        self.type = mode
        self.xmax = xmax
        self.xmin = xmin
        if self.type == "Text":
            self.surf = surface.lower()
        else:
            self.surf = surface
        
        
    def __eq__(self, other):
        return (self.uid, self.type) == (other.uid, other.type)
        
    
    def __str__(self):
        return "%s interval %s\nTime: %s-%s\nSurface: %s" % (self.type, 
                                                            self.uid,
                                                            self.xmin,
                                                            self.xmax,
                                                            self.surf)
        
    def merge(self, other):
        '''Merges two Intervals of the same type.''' 
        assert self.type == other.type # ensure similar type
        
        if self.xmin == other.xmax:    # if other->self
            self.xmin = other.xmin
            if other.surf == "":
                pass
            else:
                self.surf = other.surf + " " + self.surf
            del other
            
        elif self.xmax == other.xmin:  # if self->other
            self.xmax = other.xmax
            if other.surf == "":
                pass
            else:
                self.surf += " " + other.surf
            del other
        else:
            pass
        
        
def merge_intervals(first, second):
    '''Function that merges two Intervals using the object method'''
    first.merge(second)
    return first