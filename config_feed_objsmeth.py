# -*- mode: python; python-indent-offset: 4 -*-
''' Main and State Config File objects and methods'''


# import os
# import sys

import syslog
import copy
from operator import attrgetter
import toml
import feedparser
from SaxeBlueskyPython.ticktocktime import unix_time_now, iso_time_now
from SaxeBlueskyPython.ticktocktime import tuple_time2unix, tuple_time2iso


class MainConfigInfo:
    '''open, close, create, update, export/import info Main config file'''

    def __init__(self,main_configfile_name='salt-main.toml'):
        self.file_name = main_configfile_name

        ''' Class to manage the main config file and info'''
    @staticmethod
    def create (file2create_filename, n_feeds=1):
        '''creates a new skeletal config file
        ** Needs more detail on what to write out **
        '''


        with open (file2create_filename,'w',encoding="utf-8") as cf:
            cf.write('[GENERAL] \n')

            cf.write('Title =  " " \n')
            cf.write('Statefile =  " " \n')
            cf.write('TZ_abbr =  " " \n')
            cf.write('NumFeeds =  " " \n')
            cf.write('\n')

            cf.write('[[FEEDS]] \n')
            for i in range (0,n_feeds):
                cf.write('Name =  " " \n')
                cf.write(f'Number = {i+1} \n')
                cf.write(' \n')
                cf.write('URL =  " " \n')
                cf.write('Type =  " " \n')
                cf.write('TimeJitter =  " " \n')
                cf.write('\n')
            # end for loop
                
            cf.write('[BSKY_ACCOUNT]\n')
            cf.write('Username =  " " \n')
            cf.write('App_passwd =  " " \n')
            cf.write('Nickname =  " " \n')
            cf.write('DefaultSensitive =  " " \n')
            cf.write('\n')

            j = cf.close()

            return j

    def read (self,main_configfile_name):
        '''Reads the existing main config file and returns
                      The config info
        '''

        with open(main_configfile_name, 'r',encoding="utf-8") as mainconfigfile:
            toml_in = toml.load(mainconfigfile)
            self.config_data = toml_in
            config_data_out = copy.deepcopy(toml_in)
            mainconfigfile.close()
        return config_data_out

    @staticmethod
    def check_feed_nums (main_config_info):
        '''Read main config file and deduce number of feeds
        Main config file checking
        Takes the data structure read from the main config file
        as the argument
        '''

        j = len(main_config_info['FEEDS'])
        return j

    @staticmethod
    def write():
        ''' pass'''
        return
    
    def state_fname(self):
        self.state_file = self.config_data['GENERAL']['Statefile']
        return self.state_file

class StateConfigInfo:
    ''' Class to manage the state file and info
    ** Needs more detail on what to write out **
    self info is:
    self.state (the data read from the statefile)
    self.filename (the statfile name)
    '''
    
    def  __init__(self,file2create_filename='salt-state.toml'):
        pass
    
        

    @staticmethod
    def create (file2create_filename='salt-state.toml', n_feeds=1):
        '''creates a new skeletal state file
        with NFeeds number of feeds
        ** Needs more detail on what to write out **
        '''


        with open (file2create_filename,'w',encoding="utf-8") as cf:
            cf.write('[GENERAL] \n')
            cf.write('Title = "A title" \n')
            cf.write('\n')

            cf.write('\n')
            for i in range (0,n_feeds):
                cf.write('[[FEEDS]] \n')
                cf.write('Name = "Nick name for feed" \n')
                cf.write(f'Number = "Feed: {i+1}"  \n')
                cf.write('URL = "feed url string" \n')
                cf.write('feed_last_read_iso = "" \n')
                cf.write('feed_last_read_unix = 0 \n')
                cf.write('feed_previous_last_read_iso = "" \n')
                cf.write('feed_previous_last_read_unix = 0 \n')
                cf.write('newest_feed_item_unix = 0 \n')
                cf.write('newest_feed_item_iso = "" \n')
                cf.write('oldest_feed_item_iso = "" \n')
                cf.write('oldest_feed_item_unix = 0 \n')
                cf.write('\n')
            # End of loop


            cf.write('[BSKY_INFO] \n')
            cf.write('previous_last_posted_unix = 0 \n')
            cf.write('previous_last_posted_iso = "" \n')
            cf.write('last_posted_unix = 0 \n')
            cf.write('last_posted_iso = "" \n')
            cf.write('\n')

            j= cf.close()
            return j

    
    def read(self,filename):
        self.filename = filename
        ''' read state file '''
        with open (filename, 'r',encoding="utf-8") as stateconfigfile:
            statetoml_in = toml.load(stateconfigfile)
            self.state = statetoml_in
            stateconfigfile.close()
        return statetoml_in

    @staticmethod
    def write_info (stateoutfile_name, data2write):
        '''
        Write current state info out to file
        '''
        with open(stateoutfile_name, 'w',encoding="utf-8") as stateoutfile:
            toml.dump(data2write, stateoutfile)
            i=stateoutfile.close()
        return i

    @staticmethod
    def update_bsky_prev (info):
        '''
        takes  dict for the state file bsky info,
        updates previous last post date/times
        returns it.

        info variable is an instance of the full state file info
        '''

        info['BSKY_INFO']['previous_last_posted_unix'] \
            = info['BSKY_INFO'].get('last_posted_unix')
        info['BSKY_INFO']['previous_last_posted_iso'] \
            = info['BSKY_INFO']['last_posted_iso']

        return info

    @staticmethod
    def update_bsky_now (info):
        ''' updates post times for bsky
            info variable is an instance of the full state file info
        '''

        info['BSKY_INFO']['last_posted_unix'] = unix_time_now()
        info['BSKY_INFO']['last_posted_iso'] = iso_time_now()
        return info

    
    def check_feed_num (self):
        '''
        Checks feed numbers in STATE file
        info variable is an instance of the full state file info
        '''
        j = len(self.state['FEEDS'])
        return j

    @staticmethod
    def update_feed_prev (info):
        ''' Update timestamps of the feed read

        info variable is an instance of the full state file info
        '''
        numfeeds =  StateConfigInfo.check_feed_num (info)

        for i in range (0, numfeeds):
            info['FEEDS'][i]['feed_previous_last_read_unix'] \
                = info['FEEDS'][i]['feed_last_read_unix']
            info['FEEDS'][i]['feed_previous_last_read_iso'] \
                = info['FEEDS'][i]['feed_last_read_iso']
        # end loop

        return info

    @staticmethod
    def update_feed_now (info):
        ''' Update timestamps of the feed read
         info variable is an instance of the full state file info
        '''
        numfeeds =  StateConfigInfo.check_feed_num (info)
        for i in range (0, numfeeds):
            info['FEEDS'][i]['feed_last_read_unix'] \
                = unix_time_now()
            info['FEEDS'][i]['feed_last_read_iso'] \
                = iso_time_now()
        return info

    @staticmethod
    def update_entry_times (sorted_feeds,state_info):
        ''' update info
        Takes a feeds that has been sorted. Takes state info
        returns updated state info
        '''
        si = state_info
        sf = sorted_feeds

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
            fi = enumerate_feed_items(sf[i]) # number of feed entries

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


def chk_main_state(mainconfigfilename, stateconfigfilename):
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


    else:
        f_mci == f_sci
        return f_mci

    return f_mci

def open_read_mconfig (mainconfigfile_name):
    '''Function to read main config file
    And open state file based on info in main config file
    '''
    main_config = MainConfigInfo.read(mainconfigfile_name)
    statefile_name = main_config['GENERAL']['statefile']
    state_config = StateConfigInfo.read(statefile_name)
    configs = {
        'main_config':main_config,
        'state_config':state_config,
    }

    return configs
    # End open_read_mconfig



def find_feeds (main_config_info):
    '''Return a small structure with the feed URLs'''
    cf = main_config_info
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
    '''sort one feed
    Merge sorted entries back into feed
    '''

    sorted_entries = sorted(a_feed['entries'],
            reverse = True, key=attrgetter('published_parsed'))



    a_feed['entries'] = sorted_entries

    return a_feed

def feedHandleFetchSort (numfeeds,mainconfigdata):
    ''' this idea of rolling up these calls might not be good'''
    nf = numfeeds

    feedURLs = [0]*nf
    full_fd_content = [0]*nf
    ent_fd  = [0]*nf
    entries_per_feed =  [0]*nf
    epf = entries_per_feed #?
    # uet = [0,0]*nf # updated entry times
    # queues = [0] * nf
    feedURLs = find_feeds(mainconfigdata)

    # newrYess = [0]*nf
    for i in range (0,nf):
        full_fd_content[i]= fetch_feed(feedURLs[i])
        epf[i] = enumerate_feed_items(full_fd_content[i])
        ent_fd[i] = sort_entries(full_fd_content[i])

        sortedFeedDict = {
            'enumFeedItems': epf,
            'sortedEntries': ent_fd
        }

    return sortedFeedDict # return sorted feeds and their entries
