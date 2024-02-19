#!/usr/bin/python

"""
Goal for this test module is to pull in one post from mastodon and
repost it on bluesky.
"""
# import syslog
from SaxeBlueskyPython.ticktocktime import unix_time_now
import feedstructs
from  heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
from  heavy_lifting import MainStateConsistency, FeedEntriesMash

from operator import attrgetter
import sys
import json

MainConfigInfo.create('moo.txt')

# file name to open, number of feeds to create
rval = StateConfigInfo.create('foo.toml',3) 

t = MainConfigInfo.read('salt-main.toml')

x = StateConfigInfo.read('salt-state.toml')
x = StateConfigInfo.update_bsky_prev(x)
x = StateConfigInfo.update_bsky_now(x)
x = StateConfigInfo.update_bsky_prev(x)
x = StateConfigInfo.update_bsky_now(x)

z = StateConfigInfo.check_feed_nums(x)


foo = MainStateConsistency.feeds('salt-main.toml', 'salt-state.toml')

# exit()

numfeeds = MainConfigInfo.check_feed_nums(t)
feedURLs = MainConfigInfo.read('salt-main.toml')

# reftime = 0 # jan 1, 1970
reftime_unix = unix_time_now()

# return sorted feeds and their entries
sortedFeedDict = FetchFeeds.feedHandleFetchSort (numfeeds,
                    feedURLs,reftime_unix)


enumFeedItems = sortedFeedDict['enumFeedItems']
sortedEntries = sortedFeedDict['sortedEntries']

'''
feedURLs = [0]*hmf
full_fd_content = [0]*hmf
ent_fd  = [0]*hmf
entries_per_feed =  [0]*hmf
uet = [0,0]*hmf # updated entry times
j = entries_per_feed #??
feedURLs = FetchFeeds.find_feeds(t)

# print (feedURLs)

for i in range (0,hmf):
    
    full_fd_content[i]= FetchFeeds.fetch_feed(feedURLs[i])
    # sys.stdout.write("\n")
    # sys.stdout.write (json.dumps(fd_content[i]))
    # sys.stdout.write("\n")
    #    FetchFeeds.sort_feed(fd_content[i])
    j[i] = FetchFeeds.enumerate_feed_items(full_fd_content[i])
    ent_fd[i] = FetchFeeds.sort_entries(full_fd_content[i])
    print (json.dumps(ent_fd[i]))





# reftime = 0 # jan 1, 1970
reftime = unix_time_now()
newrYess = [0]*hmf

for i in range (0,hmf):
    newrYess[i]= FeedEntriesMash.WhichEntries2Pub(reftime, ent_fd[i])
    # The boolean list and number true in a dict
    # BoolList; NumTrue


print(newrYess)


queues = [0] * hmf
for i in range (0,hmf):
    n = newrYess[i]['NumTrue']
    if n > 0 :
        queues[i] = FeedEntriesMash.QueueFeedEntriesRaw
        (ent_fd[i],newrYess[i])
    elif n==0:
        # do nothing
        nothing = 0
    else:
        print ("this should not happen")

    print (queues[i])
    
print ()
print ()
print ('queue')
print (queues)
print (len(queues))
    
# print (json.dumps(uet))
'''

x = StateConfigInfo.read('salt-state.toml')
z = StateConfigInfo.check_feed_nums(x)


uet =StateConfigInfo.update_entry_times (sortedEntries,x)
x = StateConfigInfo.write_info('salt-state.toml',uet)
exit ()


