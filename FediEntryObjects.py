''' Fed Feed Entry Functions '''
from SaxeBlueskyPython.ticktocktime import tuple_time2unix

def check_entry2pub (fedientry,reftime):
    '''docstring here '''
    
        
    ptime = fedientry.get('published_parsed')
    utime = tuple_time2unix(ptime)
        
    if utime >= reftime:
        return bool(True)
    elif utime <= reftime:
        return bool (False)
    else:
        print ('we are lost')
    return -9

''' marking off            
def MarkEntry2Pub(self,fedientry,reftime):
    self.fedientry = fedientry
    
    pblsh_F = {
        'PutEntryInQueue': bool(False)
    }
    pblsh_T = {
        'PutEntryInQueue': bool(True)
    }

    ptime = self.fedientry.get('published_parsed')
    utime = tuple_time2unix(ptime)
        
    if utime >= reftime:
        self.fedientry.update(pblsh_T)
    elif utime <= reftime:
        self.fedientry.update(pblsh_F)
    else:
        print ('we are lost')
    return fedientry
'''



''' marking off
def ingest(self, fedpost):
    self.fedientry = fedpost
    return

def json (self):
    print (json.dumps(self.fedientry))
    # print (type(self.fedientry))
    return

def exgest(self):
    return self.fedientry
'''
