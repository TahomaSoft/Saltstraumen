"""
Modules for doing bulk of work
"""
import toml
import feedparser
import json
import syslog
from operator import attrgetter
from feedstructs import main_config_genInfo, main_config_feedInfo
from feedstructs import simple_bsky_info, state_config_genInfo
from feedstructs import feed_metadata, bsky_post_metadata
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
        main_config = readMainConfig(mainconfigfile_name)
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
        rmc = readMainConfig (MAINconfigfile_name)
        return rmc
    
    
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
        s_info = readStateConfig(filename)
        return (s_info)
          
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
    def WhichEntries2Pub(reftime, sf):
        '''Takes a reference time, in unix format'''
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
                if utime >= reftime:
                     sf[i]['entries'][j].update(pblsh_T)
                elif utime <= reftime:
                    sf[i]['entries'][j].update(pblsh_F)
                else:
                    print ('we are lost')

        return sf
    
               

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



