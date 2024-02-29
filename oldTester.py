#!/usr/bin/python3
# -*- mode: python; python-indent-offset: 4 -*-

from SaxeBlueskyPython.ticktocktime import unix_time_now, bsky_time_now
from SaxeBlueskyPython.ticktocktime import iso_zulu_time_now
from SaxeBlueskyPython.saxe_bluesky import BskyCredentials
from SaxeBlueskyPython.saxe_bluesky import BskyFeed, BskyPosts, BskyStruct

from SaxeBlueskyPython.saxeblueobjects import BskyPostPuck
from heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
import json
from heavy_lifting import MainStateConsistency, FeedEntriesMash


import inspect



# Open main config file
maincf = 'salt-main.toml'

mcfdata = MainConfigInfo.read(maincf)

# Get the state info
statecf= (mcfdata['GENERAL']['Statefile'])
scinfo = StateConfigInfo.read(statecf)

# Check main config and state file agreement
numfeedState=StateConfigInfo.check_feed_nums (scinfo)
numfeeds = MainStateConsistency.feeds (maincf, statecf)



Bcred = BskyCredentials()
acct_name = mcfdata['BSKY_ACCOUNT']['Username']
appPass = mcfdata['BSKY_ACCOUNT']['App_passwd']
Bcred.set_handle (acct_name)
Bcred.get_did ()

Bcred.set_appPW (appPass)
Bcred.start_session()
creds = Bcred.show_creds()
myPastPosts = BskyFeed.get_author_feed(creds, 2)

j = Bcred.show_creds()


# print (myPastPosts)

BskyTest = BskyPostPuck()

# BskyTest.bDataIngest (0, creds)


sessT = BskyTest.get_sessT()

for i in inspect.getmembers(BskyTest):
    print (i)
# BskyPosts.post_simple_ready (j,sessT)
