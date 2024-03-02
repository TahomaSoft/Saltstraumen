# -*- mode: python; python-indent-offset: 4 -*-
''' Main and State Config File objects and methods'''


import os
# import sys

import syslog
import copy
from operator import attrgetter
import json
import toml
import feedparser
from SaxeBlueskyPython.ticktocktime import unix_time_now, iso_time_now
from SaxeBlueskyPython.ticktocktime import tuple_time2unix, tuple_time2iso


class MainConfigInfo:
    '''open, close, create, update, export/import info Main config file
    Class to manage the main config file and info
    '''

    def __init__(self,main_configfile_name='salt-main.toml'):
        self.file_name = main_configfile_name
        self.config_data = ''
        self.feed_URLs = ''


    @staticmethod
    def create (file2create_filename, n_feeds=1):
        '''creates a new skeletal config file
        @rst
        .. hint :: ** Needs more detail on what to write out **
        '''


        with open (file2create_filename,'w',encoding="utf-8") as cf:
            cf.write('[GENERAL] \n')

            cf.write('Title =  " " \n')
            cf.write('Statefile =  " " \n')
            cf.write('TZ_abbr =  " " \n')
            cf.write('NumFeeds =  " " \n')
            cf.write('\n')

            for i in range (0,n_feeds):
                cf.write('[[FEEDS]] \n')
                cf.write('Name =  " " \n')
                cf.write(f'Number = {i+1} \n')
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

    def read (self):
        '''Reads the existing main config file and returns
                      The config info
        '''
        # check for file
        check_file = os.path.isfile(self.file_name)
        if check_file == bool(False):
            raise Exception('No Main file. ')

        with open(self.file_name, 'r',encoding="utf-8") as mainconfigfile:
            toml_in = toml.load(mainconfigfile)
            self.config_data = toml_in
            config_data_out = copy.deepcopy(toml_in)
            mainconfigfile.close()
        return config_data_out


    def check_feed_num (self):
        '''Read main config file and deduce number of feeds
        Main config file checking
        Takes the data structure read from the main config file
        as the argument
        '''

        j = len(self.config_data['FEEDS'])
        return j

    def show_feeds (self):
        '''Return a small structure with the feed URLs'''
        numfeeds = self.check_feed_num()
        cf = self.config_data

        feedURLs = [None] * numfeeds
        for i in range (0, numfeeds):
            feedURLs[i] = cf['FEEDS'][i]['URL']
        self.feed_URLs = copy.deepcopy(feedURLs)
        return feedURLs

    def write(self,filename2write):
        '''
        Write current config data out to filename2write
        '''
        with open(filename2write, 'w',encoding="utf-8") as cfo:
            #jsontest = json.dumps(self.state)
            # sfo.write(jsontest)
            toml.dump(self.config_data,cfo)
            i=cfo.close()
        return i



    def state_fname(self):
        ''' return name of the state file'''
        self.read()
        state_file = self.config_data['GENERAL']['Statefile']
        return state_file


    def print(self):
        ''' Print Self'''
        print ('Main Config Filename: ', self.file_name)
        print ('Main Config Data: ', self.config_data)
        return



class StateConfigInfo:
    '''Class to manage the state file and info

    NB:
       **Needs more detail on what to write out**

    self info is:
    * self.state_data (the data read from the statefile)
    * self.filename (the statefile name)

    '''

    def  __init__(self,state_file_name='salt-state.toml'):

        self.file_name = state_file_name
        self.state_data = ''
        self.feed_URLs = ''

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
                cf.write(f'Name = "Nick name for feed: {i+1}" \n')
                cf.write(f'Number = "Feed: {i+1}"  \n')
                cf.write(f'URL = "feed url string for feed {i+1}" \n')
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

    def add_URLs(self,Config_URLs):
        ''' tbd'''

        self.read()
        num_URLs = len (Config_URLs)
        for i in range (0, num_URLs):
            self.state_data['FEEDS'][i]['URL'] = Config_URLs[i]
        return




    def read(self):
        ''' read state file '''

        with open (self.file_name, 'r',encoding="utf-8") as stateconfigfile:
            statetoml_in = toml.load(self.file_name)
            self.state_data = statetoml_in
            stateconfigfile.close()
        return copy.deepcopy(statetoml_in)

    def print(self):
        ''' self print'''
        print ('State Filename: ', self.file_name)
        print ('State Data: ', self.state_data)
        return


    def write_state (self):
        '''
        Write current state info out to file
        '''
        with open(self.file_name, 'w',encoding="utf-8") as sfo:
            #jsontest = json.dumps(self.state)
            # sfo.write(jsontest)
            toml.dump(self.state_data,sfo)
            i=sfo.close()
        return i


    def update_bsky_prev (self):
        '''
        takes  dict for the state file bsky info,
        updates previous last post date/times
        returns it.

        info variable is an instance of the full state file info
        '''

        self.state_data['BSKY_INFO']['previous_last_posted_unix'] \
            = self.state_data['BSKY_INFO'].get('last_posted_unix')
        self.state_data['BSKY_INFO']['previous_last_posted_iso'] \
            = self.state_data['BSKY_INFO']['last_posted_iso']

        return copy.deepcopy(self.state_data)

    def update_bsky_now (self):
        ''' updates post times for bsky
            info variable is an instance of the full state file info
        '''

        self.state_data['BSKY_INFO']['last_posted_unix'] = unix_time_now()
        self.state_data['BSKY_INFO']['last_posted_iso'] = iso_time_now()

        return copy.deepcopy (self.state_data)

    def decoupled_state_data (self):
        ''' testing'''
        a = json.dumps(self.state_data)
        b = json.loads(a)
        return b

    def show_feeds (self):
        '''Return a small structure with the feed URLs'''
        numfeeds = self.check_feed_num()
        cf = self.state_data
        feedURLs = [None] * numfeeds
        for i in range (0, numfeeds):
            feedURLs[i] = cf['FEEDS'][i]['URL']
        self.feed_URLs = copy.deepcopy(feedURLs)
        return feedURLs



    def check_feed_num (self):
        '''
        Checks feed numbers in STATE file
        info variable is an instance of the full state file info
        '''
        j = len(self.state_data['FEEDS'])
        return j


    def update_feed_prev (self):
        ''' Update timestamps of the feed read

        info variable is an instance of the full state file info
        '''
        numfeeds =  self.check_feed_num ()

        for i in range (0, numfeeds):
            self.state_data['FEEDS'][i]['feed_previous_last_read_unix'] \
                = self.state_data['FEEDS'][i]['feed_last_read_unix']
            self.state_data['FEEDS'][i]['feed_previous_last_read_iso'] \
                = self.state_data['FEEDS'][i]['feed_last_read_iso']
        # end loop

        return copy.deepcopy(self.state_data)


    def update_feed_now (self):
        ''' Update timestamps of the feed read
         info variable is an instance of the full state file info
        '''
        numfeeds =  self.check_feed_num ()
        for i in range (0, numfeeds):
            self.state_data['FEEDS'][i]['feed_last_read_unix'] \
                = unix_time_now()
            self.state_data['FEEDS'][i]['feed_last_read_iso'] \
                = iso_time_now()
        return copy.deepcopy(self.state_data)


    def update_entry_times (self,sorted_feeds,entries_per_feed):
        ''' update info
        Takes a feed that has been sorted. Takes state info
        returns updated state info
        '''
        si = self.state_data
        sf = sorted_feeds
        fds = self.check_feed_num()
        epf = entries_per_feed

   
        newestEntry = [0]*fds
        oldestEntry = [0]*fds
        oeTime =  [0]*fds
        neTime = [0]*fds
        neTime_iso =  [0]*fds
        neTime_unix = [0]*fds
        oeTime_iso =  [0]*fds
        oeTime_unix = [0]*fds

        
        for i in range (0,fds):
            fi = epf[i] # number of feed entries
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

        self.state_info = si
        return si


    def get_ref_times (self):
        num_f = self.check_feed_num()
        flrtimes_unix = []
        
        for i in range (0,num_f):
            flrtimes_unix.append \
                (self.state_data['FEEDS'][i]['feed_last_read_unix'])
        return flrtimes_unix
    
# End classes
def chk_main_state (feeds_main, feeds_state):
    f_mci = feeds_main
    f_sci = feeds_state
    
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

    

    
def DePRECATEDchk_main_state(mainconfigfilename, stateconfigfilename):
    '''
    Open both the main and state config files
    from file names and check to see if feeds are consistent.
    If not consistent, throw an error and quit
    Suggest in error message to recreate state file config
    using class/routine StateConfigInfo.create
    and editing as needed
    '''


    mco = MainConfigInfo (mainconfigfilename)
    sco = StateConfigInfo (stateconfigfilename)

    mco.read()
    sco.read()

    f_mci = mco.check_feed_num
    f_sci = sco.check_feed_num

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


def find_feeds (main_config_info):
    '''Return a small structure with the feed URLs'''
    cf = main_config_info
    numfeeds = MainConfigInfo.check_feed_num(cf)
    feedURLs = [None] * numfeeds
    for i in range (0, numfeeds):
        feedURLs[i] = cf['FEEDS'][i]['URL']
    return feedURLs

def fetch_feed (URL):
    '''fetch a feed'''
    feed = feedparser.parse(URL)
    return feed

def DEPRECATEDenumerate_feed_items (feed):
    '''Describe how many entries are in a feed'''
    its = len (feed['entries'])
    return its

def DEPRECATEDsort_entries (a_feed):
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
