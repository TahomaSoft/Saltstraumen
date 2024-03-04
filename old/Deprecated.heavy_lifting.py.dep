"""
Modules for doing bulk of work
"""
import tempfile
import shutil
import html2text
import urllib.request
import toml
import feedparser
import json
import syslog
import os
from operator import attrgetter
from feedstructs import main_config_genInfo, main_config_feedInfo
from feedstructs import simple_bsky_info, state_config_genInfo
from feedstructs import feed_metadata, bsky_post_metadata
from feedstructs import post_constructor, post_media_item
from feedstructs import post_altText_plus
from SaxeBlueskyPython.ticktocktime import unix_time_now, iso_time_now
from SaxeBlueskyPython.ticktocktime import tuple_time2iso, tuple_time2unix

# Code block function to retrieve posts, sort, flag those that are newer



# code block to open up and read the config files




class MainStateConsistency:
    ''' Check to be sure both state files have right amount of feeds
    Other consistency checks:
    * feed url consistent
    * feed names consistent
    '''
    def feeds(mainconfigfilename, stateconfigfilename):
        '''
        Open both the main and state config files
        from file names and check to see if feeds are consistent.
        If not consistent, throw an error and quit
        Suggest in error message to recreate state file config
        using class/routine StateConfigInfo.create
        and editing as needed
        '''
        mci = MainConfigInfo.read(mainconfigfilename)
        sci = StateConfigInfo.read(stateconfigfilename)

        f_mci = MainConfigInfo.check_feed_nums(mci)
        f_sci = StateConfigInfo.check_feed_nums(sci)

        if f_mci != f_sci:
            print ("Main and State Config file mismatch!")
            print ("Main file lists: ",f_mci)
            print ("State file lists: ", f_sci)
            print ("Consider using StateConfigInfo.create routine ...")
            print ("To fix the problem")
            syslog.syslog (syslog.LOG_ERR,
                'SALTSTRAUMEN: Main config and \
                state file feed number mismatch')
            # effectively returns error and quits
            # return 1
            raise Exception('Config and State File feed mismatch')


        elif f_mci == f_sci:
            return f_mci


    def open_read_mconfig (mainconfigfile_name):
        '''Function to read main config file'''
        ''' And open state file based on info in main config file'''
        main_config = MainConfigInfo.readMainConfig(mainconfigfile_name)
        statefile_name = main_config['GENERAL']['statefile']
        state_config = readStateConfig(statefile_name)
        configs = {
            'main_config':main_config,
            'state_config':state_config,
        }

        return (configs)
    # End open_read_mconfig

class MainConfigInfo:

    ''' Class to manage the main config file and info'''
    def create (file2create_filename):

        '''creates a new skeletal config file'''
        a = main_config_genInfo
        b = main_config_feedInfo
        c = simple_bsky_info
        with open (file2create_filename,'w') as cf:
            cf.write('[GENERAL]')
            cf.write('\n')
            toml.dump(a,cf)
            cf.write('\n')
            cf.write('[[FEEDS]]')
            cf.write('\n')
            toml.dump(b,cf)
            cf.write('\n')
            cf.write('[BSKY_ACCOUNT]')
            cf.write('\n')
            toml.dump(c,cf)
            cf.write('\n')
            j = cf.close()
            return j


    def read (MAINconfigfile_name):
        '''Reads the existing main config file and returns
                      The config info
        '''

        with open(MAINconfigfile_name, 'r') as mainconfigfile:
            toml_in = toml.load(mainconfigfile)

            mainconfigfile.close()
        return toml_in

    # def print (self):
    #    print (self)

    def check_feed_nums (Main_config_info):
        '''Read main config file and deduce number of feeds'''
        '''Main config file checking'''
        '''
        Takes the data structure read from the main config file
        as the argument
        '''
        j = len(Main_config_info['FEEDS'])
        return j



class FetchFeeds:
    '''
    Class to Read and organize/process the incoming rss feeds
    '''
    def find_feeds (Main_config_info):
        '''Return a small structure with the feed URLs'''
        cf = Main_config_info
        numfeeds = MainConfigInfo.check_feed_nums(cf)
        feedURLs = [None] * numfeeds
        for i in range (0, numfeeds):
            feedURLs[i] = cf['FEEDS'][i]['URL']
        return feedURLs

    def fetch_feed (URL):
        '''fetch a feed'''
        feed = feedparser.parse(URL)
        return feed

    def enumerate_feed_items (feed):
        '''Describe how many entries are in a feed'''
        its = len (feed['entries'])
        return its

    def sort_entries (a_feed):
        '''sort one feed'''
        sorted_entries = sorted(a_feed['entries'],
            reverse = True, key=attrgetter('published_parsed'))
        ''' Merge sorted entries back into feed

        '''
        a_feed['entries'] = sorted_entries

        return a_feed

    def feedHandleFetchSort (numfeeds,mainconfigdata,reftime_unix):
        ''' this idea of rolling up these calls might not be good'''
        nf = numfeeds
        rft =reftime_unix

        feedURLs = [0]*nf
        full_fd_content = [0]*nf
        ent_fd  = [0]*nf
        entries_per_feed =  [0]*nf
        epf = entries_per_feed #?
        uet = [0,0]*nf # updated entry times
        queues = [0] * nf
        feedURLs = FetchFeeds.find_feeds(mainconfigdata)

        newrYess = [0]*nf
        for i in range (0,nf):
            full_fd_content[i]= FetchFeeds.fetch_feed(feedURLs[i])
            epf[i] = FetchFeeds.enumerate_feed_items(full_fd_content[i])
            ent_fd[i] = FetchFeeds.sort_entries(full_fd_content[i])

            sortedFeedDict = {
                'enumFeedItems': epf,
                'sortedEntries': ent_fd
            }

        return (sortedFeedDict) # return sorted feeds and their entries
# end class

class StateConfigInfo:
    def  __init__(self):
        self.nothing = 0

    ''' Class to manage the state file and info'''
    def create (file2create_filename, NFeeds=1):
        '''creates a new skeletal state file'''
        '''with NFeeds number of feeds'''
        a = state_config_genInfo
        b = feed_metadata
        c = bsky_post_metadata
        with open (file2create_filename,'w') as cf:
            cf.write('[GENERAL]')
            cf.write('\n')
            toml.dump(a,cf)
            cf.write('\n')
            for i in range (0,NFeeds):
                cf.write('[[FEEDS]]')
                cf.write('\n')
                toml.dump(b,cf)
                cf.write('\n')
            # end for loop

            cf.write('[BSKY_INFO]')
            cf.write('\n')
            toml.dump(c,cf)
            cf.write('\n')
            j= cf.close()
            return j


    def read(filename):
        ''' read state file '''
        with open (filename, 'r') as stateconfigfile:
            statetoml_in = toml.load(stateconfigfile)

            stateconfigfile.close()
        return statetoml_in


    def write_info (stateoutfile_name, data2write):
        '''
        Write current state info out to file
        '''
        with open(stateoutfile_name, 'w') as stateoutfile:
            toml.dump(data2write, stateoutfile)
            i=stateoutfile.close()
        return (i)


    def update_bsky_prev (info):
        '''
        takes  dict for the state file bsky info,
        updates previous last post date/times
        returns it.
        '''
        '''
        info variable is an instance of the full state file info
        '''

        info['BSKY_INFO']['previous_last_posted_unix'] \
            = info['BSKY_INFO'].get('last_posted_unix')
        info['BSKY_INFO']['previous_last_posted_iso'] \
            = info['BSKY_INFO']['last_posted_iso']

        return info

    def update_bsky_now (info):
        '''
        updates post times for bsky
        '''
        '''
        info variable is an instance of the full state file info
        '''
        info['BSKY_INFO']['last_posted_unix'] = unix_time_now()
        info['BSKY_INFO']['last_posted_iso'] = iso_time_now()
        return info

    def check_feed_nums (info):
        '''
        Checks feed numbers in STATE file
        info variable is an instance of the full state file info
        '''
        j = len(info['FEEDS'])
        return j

    def update_feed_prev (info):
        ''' Update timestamps of the feed read'''
        '''
        info variable is an instance of the full state file info
        '''
        numfeeds =  StateConfigInfo.check_feed_nums (info)

        for i in range (0, numfeeds):
            info['FEEDS'][i]['feed_previous_last_read_unix'] \
                = info['FEEDS'][i]['feed_last_read_unix']
            info['FEEDS'][i]['feed_previous_last_read_iso'] \
                = info['FEEDS'][i]['feed_last_read_iso']
        # end loop

        return info

    def update_feed_now (info):
        ''' Update timestamps of the feed read'''
        '''
        info variable is an instance of the full state file info
        '''
        numfeeds =  StateConfigInfo.check_feed_nums (info)
        for i in range (0, numfeeds):
            info['FEEDS'][i]['feed_last_read_unix'] \
                = unix_time_now()
            info['FEEDS'][i]['feed_last_read_iso'] \
                = iso_time_now()
        return info

    def update_entry_times (sorted_feeds,state_info):
        si = state_info
        sf = sorted_feeds

        '''
        Takes a feeds that has been
        sorted. Takes state info
        returns updated state info
        '''

        j = len(sf)
        newestEntry = [0]*j
        oldestEntry = [0]*j
        oeTime =  [0]*j
        neTime = [0]*j
        neTime_iso =  [0]*j
        neTime_unix = [0]*j
        oeTime_iso =  [0]*j
        oeTime_unix = [0]*j


        for i in range (0,j):
            fi = FetchFeeds.enumerate_feed_items(sf[i]) # number of feed entries

            newestEntry[i]  = sf[i]['entries'][0]
            oldestEntry[i]  = sf[i]['entries'][fi-1]

            neTime[i] = newestEntry[i]['published_parsed']
            oeTime[i] = oldestEntry[i]['published_parsed']

            neTime_iso[i] = tuple_time2iso (neTime[i])
            neTime_unix[i] = tuple_time2unix (neTime[i])
            oeTime_iso[i] = tuple_time2iso (oeTime[i])
            oeTime_unix[i] = tuple_time2unix (oeTime[i])

            si['FEEDS'][i]['newest_feed_item_unix'] = neTime_unix[i]
            si['FEEDS'][i]['newest_feed_item_iso'] = neTime_iso[i]
            si['FEEDS'][i]['oldest_feed_item_iso'] = oeTime_iso[i]
            si['FEEDS'][i]['oldest_feed_item_unix'] = oeTime_unix[i]


        return si




class FeedEntriesMash:
    def DELETEMabyeWhichEntries2Pub(reftimes, sf):
        '''Takes a reference time set (size(sf) or size (reftimes),
        in unix format'''
        '''Second argument is a singular feed to loop through
        and find entries that are later than the reftime.'''

        # sf # Sorted Feeds = sf
        sfl = len(sf)
        fi = [0] * sfl # how many entries in a feed
        pblsh_F = {
            'PutEntryInQueue': bool(False)
        }
        pblsh_T = {
            'PutEntryInQueue': bool(True)
        }

        for i in range (0,sfl):
            # number of feed entries
            fi[i] = FetchFeeds.enumerate_feed_items(sf[i])
            # print (fi[i])

        for i in range (0,sfl):
            for j in range (0,fi[i]):
                ptime = sf[i]['entries'][j]['published_parsed']
                utime = tuple_time2unix(ptime)
                if utime >= reftimes[i]:
                     sf[i]['entries'][j].update(pblsh_T)
                elif utime <= reftimes[i]:
                    sf[i]['entries'][j].update(pblsh_F)
                else:
                    print ('we are lost')

        return sf

    def DElComputeNumOutbound(f2e):
        '''Compute size of structure to hold all feed elements to be processed
        further; outbound process step one
        '''
        # f2e = feed2examine
        sfl = len(f2e)

        ec = 0

        for i in range (0, sfl):
            entnum = len (f2e[i]['entries'])
            # print (sfl, entnum)
            for j in range(0,entnum):
                if f2e[i]['entries'][j]['PutEntryInQueue']== bool(True):
                    ec = ec+1
                elif  f2e[i]['entries'][j]['PutEntryInQueue']== bool(False):
                    ec = ec # no increment
                else:
                    print ('we are lost')

        return ec

    def DEADSimplify (fI, count):
        ''' Creates outbound structure
        Takes the coarse feedIn,
        creates simpler structure
        count is number of articles to put in outbound structure
        returns outbound structure
        '''
        # P4t = Posts4Out
        # fI is feed in
        # count is how many entries in total to expect going out

        P4t = [None]
        sfl = len(fI)
        ec = 0


        for i in range (0, sfl):
            entnum = len (fI[i]['entries'])
            #print (count,sfl,i,ec, entnum)
            for j in range(0,entnum):
                 if fI[i]['entries'][j]['PutEntryInQueue']== bool(True):
                     # cleanerItem = FeedEntriesMash.Map4Simplify (fI[i]['entries'][j],ec)
                     ingest_item = fI[i]['entries'][j]
                     FFE = MiddleQueueEntry()

                     cleanerItem = FFE.entryCreate(ingest_item,ec)
                     FFE.json()


                     # P4t.append(cleanerItem)
                     ec = ec+1
                 elif fI[i]['entries'][j]['PutEntryInQueue']== bool(False):
                    ec = ec # no increment
                 else:
                    print ('we are lost')
        return P4t

    def DEADMap4Simplify(e,ec):
        # f = post_constructor
        # f ={}
        f = post_constructor
        h = html2text.HTML2Text()
        # These elements should always be present

        f['ELEMENTsequence'] = 0 + ec
        f['original_url'] = e['id']
        f['html_text'] = e['summary']


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

        # subroutines for images and associated material here
        # check to see if media attached

        if 'media_content' in e.keys(): # alternately,  e.get('media_content') != None:
            num_media =  len (e['media_content'])
            f['number_of_media'] = num_media
            media2attach = FeedEntriesMash.MediaContentAttach(e)
            f['media_array'] = media2attach

        elif e.get('media_content') == None:
            dosomething = bool (False)
            # print ('no media_content')
        else:
            print ('we are confused')

        if 'content' in e.keys():
            alt_text_collection = FeedEntriesMash.MediaContentAttachAltText(e['content'])
            f['altTextSet'] = alt_text_collection

        elif  e.get('content')  == None:
            dosomething = bool(False)
            # print ('no content')

        else:
            print ('we are confused')

        # need content warning
        # need to set sensitive_post flag as needed (true or false)

        # f['sensitive_post'] = FeedEntriesMash.Sensitive_Post_Detect(f)

        return f

    def DEADSensitive_Post_Detect (thePost):
        f = thePost
        isSensitive = bool (False)
        if f['media_rating'] != 'nonadult':
            isSensitive = bool (True)

        if f['rating'] != 'nonadult':
            isSensitive = bool (True)

        return isSensitive # boolean


    def DELETEMediaContentAttach(e):
        '''For each element entry,determine if media is present and handle it.
        Passing the info out to other routines to finish creating the outbound queue
        of reformatted fediverse elements
        '''
        ''' takes as single argument the
        '''
        mce = len (e['media_content'])
        mediaE = post_media_item

        for i in range (0, mce):
            '''
            Loop for the 'media_content' part
            '''
            medsubset = e['media_content'][i] # one set of media info
            mediaI =  FeedEntriesMash.MediaContentHandle (medsubset)
            medcont = dict(mediaI)

        else:
            donothing = True



        return  medcont

    def DELETEMediaContentAttachAltText(contentAltT):
        contloops = len (contentAltT)

        c_type =  [0] * contloops
        c_lang =  [0] * contloops
        c_base =  [0] * contloops
        c_value = [0] * contloops

        for i in range (0,contloops):
            # print
            c_type[i]=contentAltT[i]['type']
            c_lang[i]=contentAltT[i]['language']
            c_base[i]=contentAltT[i]['base']
            c_value[i]=contentAltT[i]['value']

            post_altText_plus['altText'] = c_type
            post_altText_plus['lang'] = c_lang
            post_altText_plus['base'] = c_base
            post_altText_plus['value'] = c_value

            altText_set = dict(post_altText_plus)


        return altText_set

    def ddddMediaContentHandle(MediaContentSet):
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

        filename = MediaMassage.remoteImageGet(x['media_url'])
        x['localFilePath'] = filename

        cmpFileSize = MediaMassage.CheckImageSize(filename)
        x['media_size_calculated'] = cmpFileSize


        return x

class FeedEntriesFix:
    def __init__(self):
        self.p2fix = post_constructor

    def print (self):
        print (self.p2fix)

    def echo (self):
        return self.p2fix

class MediaMassage:
    '''
    Fetch actual images from fediverse posts to place into outgoing
    '''
    def createTmpDir(dirname):
        if not os.path.exists(dirname):
            j = os.makedirs(dirname)
            return j
        elif os.path.exists(dirname):
            donothing = bool (True)

        return

    def remoteImageGet(url):
        with urllib.request.urlopen(url,data=None) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_filename:
                shutil.copyfileobj(response, tmp_filename)

        return tmp_filename.name



    def CheckImageSize(filename):
        file_stats = os.stat(filename)
        filesize = file_stats.st_size
        return filesize
