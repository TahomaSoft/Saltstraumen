#!/usr/bin/python

"""
Goal for this test module is to pull in one post from mastodon and
repost it on bluesky.
"""
# import syslog
from SaxeBlueskyPython.ticktocktime import unix_time_now
from feedstructs import post_constructor 
from heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
from heavy_lifting import MainStateConsistency, FeedEntriesMash
from heavy_lifting import MediaMassage
from operator import attrgetter
import sys
import json


# Open main config file
maincf = 'salt-main.toml'
statecf = 'salt-state.toml'

mcinfo=MainConfigInfo.read(maincf)
scinfo = StateConfigInfo.read(statecf)

numfeedState=StateConfigInfo.check_feed_nums (scinfo)

scinfo = StateConfigInfo.update_feed_prev(scinfo)
scinfo = StateConfigInfo.update_feed_now(scinfo)
checkmainfeeds = MainConfigInfo.check_feed_nums(mcinfo)

nufeeds = MainStateConsistency.feeds (maincf, statecf)

alist = FetchFeeds.find_feeds(mcinfo)

feedData = [0] * nufeeds

for i in range (0, nufeeds):
    feedData[i] = FetchFeeds.fetch_feed(alist[i])


for i in range (0, nufeeds):
    feedData[i] = FetchFeeds.sort_entries(feedData[i])

itemsPerFeed = [0] * nufeeds

for i in range (0,nufeeds):
    itemsPerFeed[i] = FetchFeeds.enumerate_feed_items(feedData[i])

# Update state file with new info from feed entries (age)
u_scinfo = StateConfigInfo.update_entry_times(feedData,scinfo)
j = StateConfigInfo.write_info(statecf, u_scinfo)

reftime = 0 # jan 1, 1970
#reftime = unix_time_now()


NeuFeedData= FeedEntriesMash.WhichEntries2Pub(reftime,feedData)

# print (json.dumps(NeuFeedData))

# find out how many articles are in the prelim queue
# create structure to hold them
# start processing article/entry by entry to put into new stack

count =  FeedEntriesMash.ComputeNumOutbound (NeuFeedData)

if count < 1:
    print ('All done. Exiting')
    exit()
    
elif count > 1:
    keepgoing = bool(True)

else:
    print ('we are lost')
    exit()


# Create a structure to hold outbound queue


    
# Now clean the entries by simplifying and such

feedIn = NeuFeedData

# Posts4Out = post_constructor 
# print (json.dumps(feedIn))

CleanerFeed = FeedEntriesMash.Simplify (feedIn, count)

print (json.dumps(CleanerFeed))
# dirname = '/tmp/saltstraumen/mediaCache'
# message = MediaMassage.createTmpDir(dirname)


