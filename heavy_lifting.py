"""
Modules for doing bulk of work
"""
import toml
import feedparser
import json
from operator import attrgetter
from feedstructs import main_config_genInfo, main_config_feedInfo
from feedstructs import simple_bsky_info, state_config_genInfo
from feedstructs import feed_metadata, bsky_post_metadata
from SaxeBlueskyPython.ticktocktime import unix_time_now, iso_time_now
from SaxeBlueskyPython.ticktocktime import tuple_time2iso, tuple_time2unix
# Code block function to retrieve posts, sort, flag those that are newer



# code block to open up and read the config files


def open_read_mconfig (mainconfigfile_name):
    '''Function to read main config file'''
    main_config = readMainConfig(mainconfigfile_name)
    statefile_name = main_config['GENERAL']['statefile']
    state_config = readStateConfig(statefile_name)
    configs = {
        'main_config':main_config,
        'state_config':state_config,
        }
    
    return (configs)


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
        rmc = readMainConfig (MAINconfigfile_name)
        return rmc

class FetchFeeds:
    '''
    Class to Read and organize/process the incoming rss feeds
    '''
    def find_feeds (Main_config_info):
        '''Return a small structure with the feed URLs'''
        cf = Main_config_info
        numfeeds = FetchFeeds.check_feed_nums(cf)
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
    
    def check_feed_nums (Main_config_info):
        '''Read main config file and deduce number of feeds'''
        j = len(Main_config_info['FEEDS'])
        return j
    
    def sort_entries (a_feed):
        '''sort one feed'''
        sorted_entries = sorted(a_feed['entries'],
            reverse = True, key=attrgetter('published_parsed'))
        # Merge sorted entries back into feed
        # print (type (a_feed))
        # print (type (sorted_entries))
        a_feed['entries'] = sorted_entries
        # print (a_feed)
        return a_feed
    
class StateConfigInfo:
    def  __init__(self):
        self.nothing = 0
        
    ''' Class to manage the state file and info'''
    def create (file2create_filename):
        '''creates a new skeletal state file'''
        a = state_config_genInfo
        b = feed_metadata
        c = bsky_post_metadata
        with open (file2create_filename,'w') as cf:
            cf.write('[GENERAL]')
            cf.write('\n')
            toml.dump(a,cf)
            cf.write('\n')
            cf.write('[[FEEDS]]')
            cf.write('\n')
            toml.dump(b,cf)
            cf.write('\n')
            cf.write('[BSKY_INFO]')
            cf.write('\n')
            toml.dump(c,cf)
            cf.write('\n')
            j= cf.close()
            return j

    def read(filename):
        ''' read state file '''
        s_info = readStateConfig(filename)
        return (s_info)
          
    def write_info (filename, data2write):
        '''
        Write current state info out to file
        '''
        
        j = writeStateConfig (filename, data2write)
        return j

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
        return (info)

    def update_entry_times (sorted_feeds,state_info):
        si = state_info
        sf = sorted_feeds
        # print (type (si))
        # print (si['FEEDS'][0])
        '''
        Takes a feeds that has been 
        sorted. Takes state info
        returns updated state info
        '''
        # print (sf[0]['entries'][0])
        # print (len(sf))
        j = len(sf)
        newestEntry = oldestEntry= [0]*j
        oeTime = neTime = [0]*j
        neTime_iso = neTime_unix = [0]*j
        oeTime_iso = oeTime_unix = [0]*j
    
        for i in range (0,j):
            fi = FetchFeeds.enumerate_feed_items(sf[i]) # number of feed entries

            # print (fi)
            newestEntry[i] = sf[i]['entries'][0]
            oldestEntry[i] = sf[i]['entries'][fi-1]

            neTime[i] = newestEntry[i]['published_parsed']
            oeTime[i] = oldestEntry[i]['published_parsed']
            # print (neTime[i])
            # print (type(neTime[i]))
            
            neTime_iso[i] = tuple_time2iso (neTime[i])
            neTime_unix[i] = tuple_time2unix (neTime[i])
            oeTime_iso[i] = tuple_time2iso (oeTime[i])
            oeTime_unix[i] = tuple_time2unix (oeTime[i])
            #  print (si)
            si['FEEDS'][i]['newest_feed_item_unix'] = neTime_unix[i]
            si['FEEDS'][i]['newest_feed_item_iso'] = neTime_iso[i]
            si['FEEDS'][i]['oldest_feed_item_iso'] = oeTime_iso[i]
            si['FEEDS'][i]['oldest_feed_item_unix'] = oeTime_unix[i]
        
        return si
    


        

    # def update_feed_now ():
    


# Smaller functions to read and write config info


def readMainConfig (mainconfigfile_name):

    with open(mainconfigfile_name, 'r') as mainconfigfile:
        toml_in = toml.load(mainconfigfile)

    mainconfigfile.close()
    return toml_in

def readStateConfig (stateconfigfile_name):

    with open (stateconfigfile_name, 'r') as stateconfigfile:
        statetoml_in = toml.load(stateconfigfile)
        # print (statetoml_in)
        stateconfigfile.close()
        return statetoml_in


def writeStateConfig (stateoutfile_name, stateData2write):
    with open(stateoutfile_name, 'w') as stateoutfile:
        toml.dump(stateData2write, stateoutfile)
        i=stateoutfile.close()
    return (i)
    



