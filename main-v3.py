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


# Open main config file
maincf='salt-main.toml'
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

# reftime = 0 # jan 1, 1970
reftime = unix_time_now()


NeuFeedData= FeedEntriesMash.WhichEntries2Pub(reftime,feedData)

print (json.dumps(NeuFeedData))




