'''Class(es) to convert partially processed fedifeed (after sorting and marking)
into a feed of bluesky posts
'''

import json


class BasicBlueskyQueue:
    ''' basic '''
    
    def __init__(self,sortedmarked_fedi_feed):
        self.raw_fedi_feed = sortedmarked_fedi_feed

    def json(self):
        ''' json print'''
        print (json.dumps(self.raw_fedi_feed))

        return
    
