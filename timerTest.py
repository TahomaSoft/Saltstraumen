#!/usr/bin/python3
# -*- mode: python; python-indent-offset: 4 -*-

''' tester for time writing '''
from heavy_lifting import MainConfigInfo, StateConfigInfo, MainStateConsistency
from heavy_lifting import FetchFeeds
import json

# Open main config file
maincf = 'salt-main.toml'
mcfdata = MainConfigInfo.read(maincf)

# Get the state info
statecf= (mcfdata['GENERAL']['Statefile'])
scinfo = StateConfigInfo.read(statecf)

# print (json.dumps(mcfdata))


# print (json.dumps(scinfo))
# Check main config and state file agreement
numfeedState=StateConfigInfo.check_feed_nums (scinfo)
numfeeds = MainStateConsistency.feeds (maincf, statecf)

# Get the URLs to pull feeds. From Main Config File info

alist=FetchFeeds.find_feeds(mcfdata)

# print (alist)
# print (nufeeds)

feedData = [0] * numfeeds
itemsPerFeed = [0] * numfeeds

for i in range (0, numfeeds):
    feedData[i] = FetchFeeds.fetch_feed(alist[i])
    feedData[i] = FetchFeeds.sort_entries(feedData[i])
    itemsPerFeed[i] = FetchFeeds.enumerate_feed_items(feedData[i])



flrtimes_unix = [0] * numfeeds
flrtimes_iso =  [0] * numfeeds
pflrtimes_u = [0] * numfeeds
pflrtimes_i = [0] * numfeeds

for i in range (0,numfeeds):
    flrtimes_unix[i] = scinfo['FEEDS'][i]['feed_last_read_unix']
    flrtimes_iso[i] = scinfo['FEEDS'][i]['feed_last_read_iso']

    pflrtimes_u[i] = scinfo['FEEDS'][i]['feed_previous_last_read_unix']
    pflrtimes_i[i] = scinfo['FEEDS'][i]['feed_previous_last_read_iso']
    # print (scinfo['FEEDS'][i]['feed_last_read_iso'])
    # print (scinfo['FEEDS'][i]['feed_previous_read_iso'])
    print (json.dumps (scinfo['FEEDS'][i]['feed_previous_last_read_iso']))
    print (pflrtimes_i[i])

print ()

# print (flrtimes_unix)
# print (flrtimes_iso)

print (pflrtimes_u)
print (pflrtimes_i)


print (json.dumps (scinfo['FEEDS'][0]['feed_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][1]['feed_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][0]['feed_previous_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][1]['feed_previous_last_read_iso']))



# print (json.dumps (scinfo['FEEDS'][2]))

exit()
