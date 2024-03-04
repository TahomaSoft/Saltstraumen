import copy
import json
from operator import attrgetter
from FediEntryObjects import check_entry2pub
from ticktocktime import tuple_time2unix

''' Feed Queues'''

class FirstFediQueue:
    ''' tbd'''
    def __init__(self, feedset):
        self.feeds = feedset
        self.num_feeds = None
        self.num_entries_feed = []
        self.sorted_feeds = copy.deepcopy(feedset)
        self.marked_feed_entries2pub = []

    def print_feeds (self):
        ''' print my feeds'''
        print (self.feeds)
        return

    def print_sorted_feeds (self):
        ''' print my feeds'''
        print (self.feeds)
        return

    def json_feeds(self):
        ''' print feeds as json'''
        print (json.dumps(self.feeds))
        return

    def json_sorted_feeds(self):
        ''' print feeds as json'''
        print (json.dumps(self.sorted_feeds))
        return

    def json_marked_queue(self):
        ''' print marked feed'''
        print (json.dumps(self.marked_feed_entries2pub))
        return

    def enumerate_feeds (self):
        ''' count number of feeds'''
        num_feeds = len (self.feeds)
        self.num_feeds = num_feeds

        return num_feeds

    def enumerate_feed_items (self):
        '''Describe how many entries are in each feed'''

        feeds = self.num_feeds

        for i in range (0, feeds):
            # print (self.feeds[i]['entries'])
            # len (self.feeds[i]['entries'])
            num_entries_feed = len (self.feeds[i]['entries'])
            self.num_entries_feed.append(num_entries_feed)

        return self.num_entries_feed

    def sort_entries (self):
        '''sort feeds, one at a time
        '''
        fl = self.num_feeds

        for i in range (0,fl):
            sorted_f = \
                sorted(self.feeds[i]['entries'], reverse = True, \
                       key=attrgetter('published_parsed'))
            self.sorted_feeds.append(sorted_f)
        # End for loop

        #self.sorted_feeds = sorted_feeds_by_time

        return self.sorted_feeds

    def mark_entries4pub (self,reftimes):
        '''docstring mark for pub, put into unified queue
        '''

        pblsh_F = {
            'PutEntryInQueue': bool(False)
        }
        pblsh_T = {
            'PutEntryInQueue': bool(True)
        }

        fl = self.num_feeds
        nef = self.num_entries_feed
        for i in range (0,fl):
            for j in range (0,nef[i]):
                fedientry = self.sorted_feeds[i]['entries'][j]

                if check_entry2pub(fedientry,reftimes[i]) == bool (True):
                    fedientry.update(pblsh_T)
                    self.marked_feed_entries2pub.append(fedientry)

                elif check_entry2pub(fedientry,reftimes[i]) == bool(False):
                    fedientry.update(pblsh_F)
                # End If


            # end inner loop
        # End outer loop

        return
