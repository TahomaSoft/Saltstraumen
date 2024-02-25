# -*- mode: python; python-indent-offset: 4 -*-
import html2text
import json
from feedstructs import post_constructor
from SaxeBlueskyPython.ticktocktime import tuple_time2iso, tuple_time2unix
import heavy_lifting
from operator import attrgetter

class BROKENMiddleQueue:
    def __init__(self):
        # joe = {}
        # fred = [joe]  * numentries
        self.fediqueue = [{}]
        
    
    def insertr (self,entry):
        print (entry)
        print (type (entry))
        print (type (self.fediqueue))
        # self.fediqueue.append(entry)
        # print (self.fediqueue)
        return
    
    def qprint (self):
        print (self.fediqueue)
        
    def json (self):
        print (json.dumps(self.fediqueue))

class BROKENMiddleQueueEntry:
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

    def entryCheck (self,rawpost):
        e = rawpost
        if e['PutEntryInQueue'] == bool(True):
            returnval = bool(True)
            
        elif e['PutEntryInQueue'] == bool(False):
            returnval = bool(False)
        else:
            print ('We are lost')

        return returnval

    def returnDict():
        return post_constructor
        
    def entryCreate(self, rawpost,seqcount):
        '''Raw post is unprocessed entry pulled from Fediverse'''
        '''seqcount is sequence count to label the entry'''
        '''returns an refined fediverse post entry for more processing'''
        
        f = post_constructor
        e = rawpost

        # print (e)
        # These elements should always be present
        
        f['ELEMENTsequence'] = seqcount
        f['original_url'] = e['id']
        f['html_text'] = e['summary']
        # self.fedipost = f
        return f

    def entryAddBasic(self,rawpost):
        h = html2text.HTML2Text()
        e = rawpost
        f = self.fedipost
        origTxt = e['summary'] 
        
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
            f['fixed_tags'] == None
            
        elif e.get('tags') != None:
            f['tags'] = e['tags']
            j = e['tags']
            f['fixed_tags'] = entryFixTags(j)
        else:
            print ('we are lost')

         # Get Summary detail
        if 'summary_detail' in e.keys():
            sd = e['summary_detail']
            f['base_post_mime_t'] = sd['type']
            f['alt_lang_post'] = sd['language']
            f['base_url'] = sd['base']
            f['html_text_sdetail'] = sd['value']

        # check for content warning in original html_text
        txtCWtpl = cw_check (origTxt)
        contentWarn = txtCWtpl[0]
        cleanMainTxt = txtCWtpl[1]
        f['content_warn'] = contentWarn
        f['contentWarn'] = contentWarn
        f['basic_text_rev'] = cleanMainTxt
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
        self.AmFeeds = feeds # Amended feed. simplify later
        self.feedQ = len (feeds)
        self.counter = [0] * self.feedQ
        self.UniFeed = []
        
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
    
    def concatFeeds (self):
        UniFeed = []
        for i in self.AmFeeds:
            # print (i)
            UniFeed.append(i)
            self.UniFeed = UniFeed
        # print (self.UniFeed)
        return UniFeed
        
    def feedcounts(self):
        
        counter = [0] * self.feedQ
        i =0
        
        for i in range (0, self.feedQ):
            str_tmp = self.feeds[i] 
            j = len(str_tmp)
            counter[i] = {'feedN': i,'numE': j}
        # end for loop
              
        self.counter=counter
        
        return self.counter
                                            
    
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

    def DEELETEdorkcomputeTrue (self):
        # Simiplify this amFeeds thing later
        # using a copy after adding true/false pub info
        # 'cause that step flattened the structure by accident
        actr = 0
        for i in range (0, self.feedQ):
            z = self.counter[i]['numE']
            for j in range (0,z):
                if self.AmFeeds[i][j]['PutEntryInQueue'] == bool (True):
                    actr = actr +1
                elif self.AmFeeds[i][j]['PutEntryInQueue'] == bool (False):
                    donothing = 1
                else:
                    print ('We are lost')
        # end outer loop
        self.numtrue = actr
        return actr

    def newQueue (self,entry):
        self.UniFeed.append(entry)
        # print (entry)
        return
    
    def newQueueExgest (self,i):
       return self.UniFeed[i]
   
    
class FedFeedEntry:
    def __init__(self):
        self.fedientry = {}

    def checkEntry2Pub (self,fedientry,reftime):
        self.fedientry = fedientry
        
        ptime = self.fedientry.get('published_parsed')
        utime = tuple_time2unix(ptime)
        
        if utime >= reftime:
            return bool(True)
        elif utime <= reftime:
            return bool (False)
        else:
            print ('we are lost')
        return (-9)
            
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
    
    def ingest(self, fedpost):
        self.fedientry = fedpost
        return

    def json (self):
        print (json.dumps(self.fedientry))
        # print (type(self.fedientry))
        return

    def exgest(self):
        return self.fedientry

# End Classes

def entryFixTags (tagstring):
    '''mzonePost is output from entryAddBasic'''
    ''' take tags and write fixed_tags'''
    # print (tagstring)
    ts =''
    l = len (tagstring)
    for i in range (0,l):
        # print (tagstring[i])
        j= tagstring[i]['term']
        ts = ts +' ' + j
        
    fixedTag = ts
    
    return fixedTag
            
def cw_check (origTxt):
    h = html2text.HTML2Text()
    
    '''
    check for html string '<hr />'
    indicates text left of it is a content warning
    '''
    if '<hr />' in origTxt:
        # print ('DANGER DANGER DANGER \n \n ')
        hrLoc=origTxt.find('<hr />')
        # get substring up to that spot

        cw_html =origTxt[0:hrLoc]# origTxt.slice(0,hrLoc,1)
        # print (cw_html)
        # then convert html to basic text
        cw = h.handle(cw_html)
        bodyHtxt = origTxt[hrLoc]
        
           
    else:
        cw = ''
        bodyHtxt = origTxt
        bodytxt = h.handle(bodyHtxt)
        
    if '<a class="mention hashtag"' in bodyHtxt:
        jnkStrt = bodyHtxt.find('<a class="mention hashtag"')
        jnkStp  = bodyHtxt.find('<span>') + 6  # count <span> too
        bdyHcln = bodyHtxt[0:jnkStrt] + bodyHtxt[jnkStp:]
        
        if '<a class="mention hashtag"' in bdyHcln: # repeat
            bodyHtxt = bdyHcln

            jnkStrt = bodyHtxt.find('<a class="mention hashtag"')
            jnkStp  = bodyHtxt.find('<span>') + 6  # count <span> too
            bdyHcln = bodyHtxt[0:jnkStrt] + bodyHtxt[jnkStp:]
        
    #else:
    bodyHcln = bodyHtxt
    bodytxt = h.handle(bodyHcln)
        
    tupletext = (cw, bodytxt)
    
    return tupletext

def entryCreate(rawpost,seqcount):
    '''Raw post is unprocessed entry pulled from Fediverse'''
    '''seqcount is sequence count to label the entry'''
    '''returns an refined fediverse post entry for more processing'''
        
    f = {
        'ELEMENTsequence': 0,
        'original_url': 0,
        'html_text': 0
        }

    i = seqcount
    
    e = rawpost
    
    # print (e)
    # These elements should always be present
    
    f['ELEMENTsequence'] = i
    f['original_url'] = e['id']
    f['html_text'] = e['summary']

    g = entryAddBasic (e)
    f.update (g)
    h = entryAddRatings (e)
    if h != None:
        f.update(h)
    # check h, then update

    aSD = addSummaryDetail(e)
    f.update(aSD)

    CWinfo = addContentWarning(f['html_text'])
    f.update(CWinfo)
    
    return f

def entryAddBasic(rawpost):
    h = html2text.HTML2Text()
    e = rawpost
    
    origTxt = e['summary']

    g = {
        'basic_text': 'string',
        'lang_of_post': 'string',
        'base_url': 'base location of feed',
        'published_parsed': 'published parsed python',
        'orig_post_time': 'convert to unixtime'
        }
    
    
    tmp = h.handle(e['summary']) # remove html
    g['basic_text'] = tmp.strip() # remove new lines using strip
    g['lang_of_post'] = e['summary_detail']['language'] # as of feb 2024, usually = none
    g['base_url'] = e ['summary_detail']['base']
    g['published_parsed'] = e['published_parsed']
    g['orig_post_time'] = tuple_time2unix (e['published_parsed'])
    
    return g


def entryAddRatings (rawpost):
    #  These elements are conditional; need to check and handle absent/present'''
    e = rawpost
    MRat = {}

    r = {'rating': ''}
    
    mr = {'media_rating':''}
    
    t = {'tags':''}

    ft = {'fixed_tags':''}
        
    
    if e.get('media_rating') != None:
        mr['media_rating'] = e['media_rating']['content']
        MRat.update(mr)
        
    elif e.get('media_rating') == None:
        mr['media_rating'] = 'nonadult'
        MRat.update(mr)
         
    if e.get('rating') != None:
        r['rating'] = e['rating']
        MRat.update (r)       
    elif e.get('rating') == None:
        r['rating'] = 'nonadult'
        MRat.update (r)
    if e.get('tags') == None:
        ft['fixed_tags'] == None
        MRat.update (ft)
    elif e.get('tags') != None:
        t['tags'] = e['tags']
        MRat.update(t)
        j = e['tags']
        #ft['fixed_tags'] = entryFixTags(j)
    else:
        print ('we are lost')
       
     
    return MRat

def addSummaryDetail(rawpost):

    e = rawpost
    
    aSD = {}

    f = {
        'summary_detail': '',
        'base_post_mime_t': '',
        'alt_lang_post': '',
        'base_url': '',
        'html_text_sdetail': ''
        }
        
    # Get Summary detail
    if 'summary_detail' in e.keys():
        sd = e['summary_detail']
        f['base_post_mime_t'] = sd['type']
        f['alt_lang_post'] = sd['language']
        f['base_url'] = sd['base']
        f['html_text_sdetail'] = sd['value']
    # end if

    aSD.update (f)
    return aSD

def addContentWarning (origTxt):

    CW ={}
    cw = {
        'content_warn': '',
        'contentWarn': '',
        'basic_text_rev': ''
    }

    # check for content warning in original html_text
    txtCWtpl = cw_check (origTxt)
    contentWarn = txtCWtpl[0]
    cleanMainTxt = txtCWtpl[1]
    cw['content_warn'] = contentWarn
    cw['contentWarn'] = contentWarn
    cw['basic_text_rev'] = cleanMainTxt
    CW.update (cw)
    return CW
