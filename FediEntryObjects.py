''' Fed Feed Entry Functions '''
from ticktocktime import tuple_time2unix

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

