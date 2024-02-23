# -*- mode: python; python-indent-offset: 4 -*-

from SaxeBlueskyPython.ticktocktime import bsky_time_now
from SaxeBlueskyPython.saxe_bluesky import  basic_post_dict
import json

class PostXwalk:
    def __init__(self):
        
        self.bpost = basic_post_dict
         
    def print (self):
        print(self.bpost)
        
    def mapper_main (FediPost, BluePost):
        x = 0
        ''' takes a single Fediverse post and creates
        a single BlueSky Post 
        '''

        return BluePost
    
    def simple_p_map (FediPost, BluePost):
        F = FediPost
        B = BluePost

    def addDID (self,mainCredsDID):
        did = mainCredsDID
        self.bpost['repo'] = did
        return 
        
    def addText (self,textString):
        self.bpost['record']['text'] = textString
        return

    def stringsize (self):
        return len (self.bpost['record']['text'])
    
    def addTime (self):
        now = bsky_time_now()
        self.bpost['record']['createdAt'] = now 
        return bsky_time_now()

    def ignore (self):
        '''These aren't variables now,already set in constructor'''
        self.bpost['collection'] =  'app.bsky.feed.post'
        self.bpost['validate'] = bool(True)
        self.bpost['labels'] =[]
        return
    
    def echo (self):
        return self.bpost

    def json (self):
        return json.dumps(self.bpost)

    
