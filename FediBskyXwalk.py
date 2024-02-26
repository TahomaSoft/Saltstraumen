# -*- mode: python; python-indent-offset: 4 -*-

from SaxeBlueskyPython.ticktocktime import bsky_time_now
from SaxeBlueskyPython.saxe_bluesky import  basic_post_dict
import json

class PostXwalk:
    def __init__(self):
        
        self.bpost = basic_post_dict
        # self.bpost['gotBlob'] = bool (False)
        
    def print (self):
        print(self.bpost)
        
    def mapper_main (self,FediPost):
        ''' takes a single Fediverse post and creates
        a single BlueSky Post 
        '''
        F = FediPost
        return

    
    def simple_p_map (self, FediPost):
        F = FediPost

        ''' takes a single Fediverse post and creates
        a single BlueSky Post 
        '''

        '''these items should not be hit or miss'''
        '''those hit/miss items will be in a differnent method'''
        
        F = FediPost
        # self = Bsky Post
        self.bpost['fediPostItems']['textReady2Post'] \
            = F['textReady2Post']
       
        self.bpost['fediPostItems']['base_url'] \
            = F['base_url']
        
        self.bpost['fediPostItems']['orig_post_time'] \
            = F['orig_post_time']

        self.bpost['fediPostItems']['sensitive_post'] \
            = F['sensitive_post']
                 
        return
    
    def extendedF2Pmap (self, FediPost):
        F = FediPost
        if not F['fixed_tags']:
            skip = 1

        elif F['fixed_tags']:
            self.bpost['fediPostItems']['fixed_tags'] \
                = F['fixed_tags']
            
        if not F['media_rating']:
            skip = 1
            
        elif F['media_rating']:
            self.bpost['fediPostItems']['media_rating'] \
                = F['media_rating']
                   
        if not F['base_post_mime_t']:
            skip = 1
            
        elif F['base_post_mime_t']:
            self.bpost['fediPostItems']['base_post_mime_t'] \
                = F['base_post_mime_t']
            
        return

    def addDID (self,mainCredsDID):
        did = mainCredsDID
        self.bpost['repo'] = did
        return 
        
    def addTextRaw (self,textString):
        self.bpost['raw_text'] = textString
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
    
    def bEcho (self):
        retval = self.bpost['fediPostItems']['textReady2Post']
        return retval


    def json (self):
        return json.dumps(self.bpost)

    def addBlobFlag (self, ifBlobBool):
        self.bpost['gotBlob'] = ifBlobBool
        return

    def checkBlobFlag (self):
        return self.bpost['gotBlob']

    def checkSensitive (self):
        retval = self.bpost['fediPostItems']['sensitive_post'] 
        return 
    
    def addBlobInfo (self, blobstuff):
        numBlobs1 = len (blobstuff['media_content'])
        numBlobs2 = len (blobstuff['SetMediaElements'])
        mcBlobs = blobstuff['media_content']
        SMEblobs = blobstuff['SetMediaElements']
        if numBlobs2 > 4:
            print ("Only can publish up to 4 elements per post")
            numBlob2 =4
        # endif
        blobinfo = {
            'media_size_stated':None,
            'media_size_calculated':None,
            'medium_type': None,
            'localFilePath':None
        }
            
        blobinfos = []
        for i in range (0, numBlobs2):
           
            
            
            blobinfo['media_size_stated'] = SMEblobs[i]['media_size_stated']
            blobinfo['media_size_calculated'] = \
                SMEblobs[i]['media_size_calculated']
            blobinfo['medium_type'] = SMEblobs[i]['medium_type']
            blobinfo['localFilePath']= SMEblobs[i]['localFilePath']
        

        # end for
            blobinfos.append(blobinfo)
            self.blobinfos = blobinfos
        return
