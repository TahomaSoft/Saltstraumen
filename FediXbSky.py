'''Class(es) to convert partially processed fedifeed (after sorting and marking)
into a feed of bluesky posts
'''
import os
import shutil
import urllib.request
import tempfile
import json
import pandoc
from  html2text import HTML2Text

from ticktocktime import bsky_time_now, tuple_time2unix

class BasicBlueskyQueue:
    ''' basic queue holder'''

    def __init__(self,sortedmarked_fedi_feed):
        self.raw_fedi_feed = sortedmarked_fedi_feed
        self.first_pass_queue = []

    def json_raw(self):
        ''' json print raw queue'''
        print (json.dumps(self.raw_fedi_feed))
        return

    def json_firstpassq(self):
        ''' json print first pass queue'''
        print (json.dumps(self.first_pass_queue))
        return

    def queue_itm_exgest(self,index):
        ''' return element of the first pass queue'''
        i = index
        j = self.first_pass_queue[i]
        return j
        

    def queue_sze (self):
        j = len(self.first_pass_queue)
        return j

    def first_clean(self):
        ''' tbd'''

        for i in self.raw_fedi_feed:
            enry = FirstEntryXwalk(i)
            j = enry.mapper()
            # print ()
            # print ("*********************")
            # print (j)
            # print()
            #print (type(j))
            
            self.first_pass_queue.append(j)
        return

    

class FirstEntryXwalk:
    '''class for working on initial fediverse to
    bluesky entry crosswalk.
    This is a class for an entry, not a queue
    '''

    def __init__(self, entry):
        self.entry = entry
        self.exit = {}

    def json_entry(self):
        ''' Diagnostic printing using json'''
        print (json.dumps(self.entry))
        return

    def mapper(self):
        '''Main mapper function'''

        concat = {}
        bsc = entryAddBasic(self.entry)
        rts = entryAddRatings(self.entry)
        acw = entry_cw_check(self.entry)
        concat.update(bsc)
        concat.update(rts)
        concat.update(acw)

        check_sensitive = entryCheckSensitive(concat)
        concat.update(check_sensitive)

        is_media = MediaContentCheck(self.entry)
        if is_media == bool (True):
            media_added = MediaContentAttach(self.entry)
            concat.update(media_added)

        elif is_media == bool(False):
            skip = 1


        self.exit = concat

        return self.exit

    def data_export (self):
        ''' Export data to post builders '''
        return


# End Classess

# Start Functions

def export_basic(entry):

    return
    
def export_media(entry):
    return
    

def MediaContentCheck (element):

    if element.get('media_content') == None:
        got_media = bool (False)
    elif element.get('media_content') != None:
        got_media = bool (True)

    return got_media


def MediaContentAttach (medElem):
    '''For each element entry,determine if media is present and handle it.'''
    ''' Needs to handle a media sets from 1 to ...'''
    ''' Check for presense of media is needed before invoking this'''
    ''' is working on the middle queue'''
    numContent = len (medElem['media_content'])
    medContent = medElem['media_content']
    stru2ret = {'SetMediaElements':''}
    innrLst = []
    innrDict = {}

    #print (numContent)
    for i in range (0, numContent):
        mediaInfo = MediaContentHandle (medContent[i])
        innrDict.update (mediaInfo)
        note = {'Entry':i+1, 'Of':numContent}
        innrDict.update (note)
        innrLst.append(innrDict)
    stru2ret['SetMediaElements'] =innrLst
    medElem.update(stru2ret)
    # print (medElem)
    return medElem

def MediaContentHandle(MediaContentSet):
    # x is revised media material
    y = MediaContentSet

    x = {
        'media_url': y['url'],
        'media_type': y['type'],
        'media_size_stated': y['filesize'],
        'media_size_calculated': 'reserved',
        'medium_type': y['medium'],
        'localFilePath': 'reserved',
    }

    filename = remoteImageGet(x['media_url'])
    x['localFilePath'] = filename

    cmpFileSize = CheckImageSize(filename)
    x['media_size_calculated'] = cmpFileSize


    return x

def entryAddBasic(rawpost):
    ''' Starting process of transforming fedi post to bsky post
    does the super basic, should always be there fields.
    NB: current use of html2text needs improvement.
    First cut: use option to remove links
    Second cut: use pandoc
    Third idea: combine html2text and pandoc
    '''

    h = HTML2Text()
    e = rawpost

    # origTxt = e['summary']

    g = {
        'orig_text': 'html_laden_string',
        'basic_text': 'string',
        'lang_of_post': 'string',
        'base_url': 'base location of feed',
        'published_parsed': 'published parsed python',
        'orig_post_time': 'convert to unixtime',
        'SetMediaElements': 'placeholder for media if present'
        }

    g['orig_text'] = e['summary']
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
        ft['fixed_tags'] = entryFixTags(j)

        MRat.update (ft)
    else:
        print ('we are lost')


    return MRat

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

def entry_cw_check (rawpost): # Change this to rawpost
    '''
    check for html string '<hr />'
    indicates text left of it is a content warning
    '''


    e = rawpost
    h = HTML2Text()
    g = {
        'content_warn': 'content_warning if any',
        'basic_text_rev': 'revised version of basic text, after cw filtering',
        }
    origTxt = e['summary']

    if '<hr />' in origTxt:

        hrLoc=origTxt.find('<hr />')
        # get substring up to that spot

        cw_html =origTxt[0:hrLoc]# origTxt.slice(0,hrLoc,1)
        # print (cw_html)
        # then convert html to basic text
        cw = h.handle(cw_html)
        bodyHtxt = origTxt[hrLoc:]
        bodytxt = h.handle(bodyHtxt)

    else:
        cw = ''
        bodyHtxt = origTxt
        bodytxt = h.handle(bodyHtxt)



    g['content_warn']= cw
    g['basic_text_rev'] = bodytxt
    cw_text_dict = g

    return cw_text_dict

def entryCheckSensitive(cleanerPost):

    f = cleanerPost
    isSensitive = bool (False)

    if f['media_rating'] != 'nonadult':
        isSensitive = bool (True)

    if f['rating'] != 'nonadult':
        isSensitive = bool (True)

    if f['content_warn'] != '':
        isSensitive = bool (True)

    spost = {
        'sensitive_post': isSensitive
    }

    return spost




def remoteImageGet(url):
    '''
    Fetch actual images from fediverse posts to place into outgoing
    '''

    with urllib.request.urlopen(url,data=None) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_filename:
            shutil.copyfileobj(response, tmp_filename)

    return tmp_filename.name



def CheckImageSize(filename):
    file_stats = os.stat(filename)
    filesize = file_stats.st_size
    return filesize
