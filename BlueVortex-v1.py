#!/usr/bin/python3
# -*- mode: python; python-indent-offset: 4 -*-


'''
First attempt to integrate saltstraumen and saxe-bluesky
to read posts from a user's public Mastodon rss feed (saltstraumen),
and post to BlueSky (SaxeBlueskyPython)
'''

from FediBskyXwalk import PostXwalk

from heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
from heavy_lifting import MainStateConsistency, FeedEntriesMash
from heavy_lifting import MediaMassage
from SaxeBlueskyPython.ticktocktime import unix_time_now, bsky_time_now
from SaxeBlueskyPython.ticktocktime import iso_zulu_time_now
from SaxeBlueskyPython.saxe_bluesky import BskyCredentials
from SaxeBlueskyPython.saxe_bluesky import BskyFeed, BskyPosts, BskyStruct
import json


# Open main config file
maincf = 'salt-main.toml'

mcfdata = MainConfigInfo.read(maincf)

# Get the state info
statecf= (mcfdata['GENERAL']['Statefile'])
scinfo = StateConfigInfo.read(statecf)

# Check main config and state file agreement
numfeedState=StateConfigInfo.check_feed_nums (scinfo)
nufeeds = MainStateConsistency.feeds (maincf, statecf)

# Get the URLs to pull feeds. From Main Config File info

alist=FetchFeeds.find_feeds(mcfdata)

# create structures to hold the feeds, fetch and sort

feedData = [0] * nufeeds

for i in range (0, nufeeds):
    feedData[i] = FetchFeeds.fetch_feed(alist[i])

for i in range (0, nufeeds):
    feedData[i] = FetchFeeds.sort_entries(feedData[i])

itemsPerFeed = [0] * nufeeds

for i in range (0,nufeeds):
    itemsPerFeed[i] = FetchFeeds.enumerate_feed_items(feedData[i])

# Get the reference time to compare the last feed pulls too
# In production, get that from the state file

reftimes = [0] * nufeeds

for i in range (0,nufeeds):
    reftimes[i] = scinfo['FEEDS'][i].get('feed_last_read_unix')

# print (reftimes)

# reftimes = [0,0] # jan 1, 1970
now1 = unix_time_now()
now2 = unix_time_now()
# reftimes = [now1,now2]

    
# Note: rss feed from mastodon has only public feeds by design

# Update read times for feeds in state file
scinfo = StateConfigInfo.update_feed_prev(scinfo)
scinfo = StateConfigInfo.update_feed_now(scinfo)

# Update state file with new info from feed entries (age)
u_scinfo = StateConfigInfo.update_entry_times(feedData,scinfo)
j = StateConfigInfo.write_info(statecf, u_scinfo)

NeuFeedData= FeedEntriesMash.WhichEntries2Pub(reftimes,feedData)


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

FediP = FeedEntriesMash.Simplify (NeuFeedData, count)





Bcred = BskyCredentials()

# print (mcfdata['BSKY_ACCOUNT'])
acct_name = mcfdata['BSKY_ACCOUNT']['Username']


Bcred.set_handle (acct_name)



appPass = mcfdata['BSKY_ACCOUNT']['App_passwd']

Bcred.get_did ()
Bcred.set_appPW (appPass)
Bcred.start_session()

# Bcred.printCred()
creds = Bcred.show_creds()

myPastPosts = BskyFeed.get_author_feed(creds, 20)

# fred = BskyStruct()
# sally = fred.INIT()
# print (sally)

# print (json.dumps(myPastPosts))
bpost = PostXwalk()

# bposts = [bpost] * count
sessT = Bcred.get_sessT()

myDID = Bcred.myDID()


for i in range (0,count):

    bpost.addDID(myDID)

    bpost.addText(FediP[i]['basic_text'])
    bpost.addTime()
    
    BskyPosts.post_simple_ready (bpost,sessT)


