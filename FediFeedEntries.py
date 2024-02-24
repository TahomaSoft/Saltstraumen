# -*- mode: python; python-indent-offset: 4 -*-
import html2text
import json
from feedstructs import post_constructor
from SaxeBlueskyPython.ticktocktime import tuple_time2iso, tuple_time2unix
import heavy_lifting
from operator import attrgetter


class MiddleQueueEntry:
    ''' works on a single entry'''
    ''' Is an interim step between what is pulled from fediverse'''
    ''' and what goes for further transliteration or processing '''
    ''' an entry is a single post'''

    
    def __init__(self):
        self.fedipost = {}
        
    def echo (self):
        return self.fedipost
    
    def print (self):
        print (self.fedipost)
        return

    def json (self):
        print ("llll")
        print (json.dumps(self.fedipost))
        print ('jjjjj')
        return 

    def entryCreate(self,rawpost,seqcount):
        '''Raw post is unprocessed entry pulled from Fediverse'''
        '''seqcount is sequence count to label the entry'''
        '''returns an refined fediverse post entry for more processing'''
        
        f = self.fedipost
        e = rawpost
        
        # These elements should always be present
        
        f['ELEMENTsequence'] = seqcount
        f['original_url'] = e['id']
        f['html_text'] = e['summary']
        return f

    def entryAddBasic(self,rawpost):
        h = html2text.HTML2Text()
        e = rawpost
        f = self.fedipost
        
        tmp = h.handle(e['summary']) # remove html
        f['basic_text'] = tmp.strip() # remove new lines using strip
        f['lang_of_post'] = e['summary_detail']['language'] # as of feb 2024, usually = none
        f['base_url'] = e ['summary_detail']['base']
        f['published_parsed'] = e['published_parsed']
        f['orig_post_time'] = tuple_time2unix (e['published_parsed'])

        # These elements are conditional; need to check and handle absent/present
        # print (e.get('media_rating'))
        if e.get('media_rating') != None:
            f['media_rating'] = e['media_rating']['content']

        elif e.get('media_rating') == None:
            f['media_rating'] = 'nonadult'

        if e.get('rating') != None:
            f['rating'] = e['rating']

        elif e.get('rating') == None:
            f['rating'] = 'nonadult'
            
        if e.get('tags') == None:
            zeros = 0 # Do nothing

        elif e.get('tags') != None:
            f['tags'] = e['tags']

        else:
            print ('we are lost')

         # Get Summary detail
        if 'summary_detail' in e.keys():
            sd = e['summary_detail']
            f['base_post_mime_t'] = sd['type']
            f['alt_lang_post'] = sd['language']
            f['base_url'] = sd['base']
            f['html_text_sdetail'] = sd['value']
        return f

    def entryAddImages(self,rawpost):
        f = self
        e = rawpost
        
        # subroutines for images and associated material here
        # check to see if media attached

        if 'media_content' in e.keys(): # alternately,  e.get('media_content') != None:
            num_media =  len (e['media_content'])
            f['number_of_media'] = num_media
            # media2attach = FeedEntriesMash.MediaContentAttach(e)
            # f['media_array'] = media2attach
            
        elif e.get('media_content') == None:
            dosomething = bool (False)
            # print ('no media_content')
        else:            
            print ('we are confused')

        if 'content' in e.keys():
            # alt_text_collection = FeedEntriesMash.MediaContentAttachAltText(e['content'])            
            # f['altTextSet'] = alt_text_collection
            donothingnow = bool(True)
            
        elif  e.get('content')  == None:
            dosomething = bool(False)
            # print ('no content')

        else:            
            print ('we are confused')
            
        return f

    def entrySetSensitive(self,rawpost):
        placeholder = 1
        # need content warning
        # need to set sensitive_post flag as needed (true or false)
            
        # f['sensitive_post'] = FeedEntriesMash.Sensitive_Post_Detect(f)
        return

class HolderFedFeed:
    def __init__(self,feeds):
        self.feeds = feeds
        self.feedQ = len (feeds)
        
    def json (self):
        print (json.dumps(self.feeds))
        return
    
    def checknumfeeds_ex(self,stateinfo):
        from heavy_lifting import StateConfigInfo
        t = StateConfigInfo.check_feed_nums(stateinfo)
        self.feedQ = t
        return t

    def checknumfeeds_in(self):
        j= len (self.feeds)
        return j

    def feedcounts(self):
        
        counter = [0] * self.feedQ
        print (counter)
        i =0
        print (self.feedQ)
        for i in range (0, self.feedQ):
            counter[i] = {
                'feedN' : i,
                'numE': i + 565
            }
            
        # now put in real count of elements.
        print (counter)
        return 
                                            
    
    def sort_entries (self):
        '''sort one feed'''
        sorted_entries = self.feeds
        
        for i in range (0,self.feedQ):
            
            sorted_entries[i] = sorted(self.feeds[i]['entries'],
                reverse = True, key=attrgetter('published_parsed'))

        ''' Merge sorted entries back into feed'''
        self.feeds = sorted_entries

        return sorted_entries

    def exgest (self):
        return self

    def exportFeeds (self):
        return self.feeds
    
       
    
class FedFeedEntry:
    def __init__(self, fedientry):
        self.fedientry = fedientry
        
    def MarkEntry2Pub(self,reftime):
        pblsh_F = {
            'PutEntryInQueue': bool(False)
        }
        pblsh_T = {
            'PutEntryInQueue': bool(True)
        }

        ptime = self.fedientry['published_parsed']
        utime = tuple_time2unix(ptime)
        
        if utime >= reftime:
            self.update(pblsh_T)
        elif utime <= reftime:
            self.update(pblsh_F)
        else:
            print ('we are lost')
        return sf
    
    def ingest(self, fedpost):
        self.fedientry = fedpost
        return

    def json (self):
        print (json.dumps(self.fedientry))
        return

    def exgest(self):
        return self.fedientry
