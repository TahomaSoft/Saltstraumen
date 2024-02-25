#!/usr/bin/python3
# -*- mode: python; python-indent-offset: 4 -*-


'''
First attempt to integrate saltstraumen and saxe-bluesky
to read posts from a user's public Mastodon rss feed (saltstraumen),
and post to BlueSky (SaxeBlueskyPython)
'''

from FediBskyXwalk import PostXwalk
from feedstructs import post_constructor
from heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
from heavy_lifting import MainStateConsistency, FeedEntriesMash
from heavy_lifting import MediaMassage
from SaxeBlueskyPython.ticktocktime import unix_time_now, bsky_time_now
from SaxeBlueskyPython.ticktocktime import iso_zulu_time_now
from SaxeBlueskyPython.saxe_bluesky import BskyCredentials
from SaxeBlueskyPython.saxe_bluesky import BskyFeed, BskyPosts, BskyStruct
import json
from FediFeedEntries import HolderFedFeed, FedFeedEntry
from FediFeedEntries import entryCreate

# Open main config file
maincf = 'salt-main.toml'

mcfdata = MainConfigInfo.read(maincf)

# Get the state info
statecf= (mcfdata['GENERAL']['Statefile'])
scinfo = StateConfigInfo.read(statecf)

# Check main config and state file agreement
numfeedState=StateConfigInfo.check_feed_nums (scinfo)
numfeeds = MainStateConsistency.feeds (maincf, statecf)

# Get the URLs to pull feeds. From Main Config File info

alist=FetchFeeds.find_feeds(mcfdata)

# create structures to hold the feeds, fetch and sort

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

# Get the reference time to compare the last feed pulls too
# In production, get that from the state file


for i in range (0,numfeeds):
    flrtimes_unix[i] = scinfo['FEEDS'][i]['feed_last_read_unix']
    flrtimes_iso[i] = scinfo['FEEDS'][i]['feed_last_read_iso']

    pflrtimes_u[i] = scinfo['FEEDS'][i]['feed_previous_last_read_unix']
    pflrtimes_i[i] = scinfo['FEEDS'][i]['feed_previous_last_read_iso']



# times for testing  

# reftimes = [0,0] # jan 1, 1970
now1 = unix_time_now()
now2 = unix_time_now()
# reftimes = [now1,now2]

'''
print (pflrtimes_u)
print (pflrtimes_i)


print (json.dumps (scinfo['FEEDS'][0]['feed_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][1]['feed_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][0]['feed_previous_last_read_iso']))
print (json.dumps (scinfo['FEEDS'][1]['feed_previous_last_read_iso']))
'''


# Note: rss feed from mastodon has only public feeds by design

# Update read times for feeds in state file
scinfo = StateConfigInfo.update_feed_prev(scinfo)
scinfo = StateConfigInfo.update_feed_now(scinfo)

# Update state file with new info from feed entries (age)
u_scinfo = StateConfigInfo.update_entry_times(feedData,scinfo)
j = StateConfigInfo.write_info(statecf, u_scinfo)

# print ("........")
# print ("........")


#print (pflrtimes_u)
# print (pflrtimes_i)


# print (json.dumps (scinfo['FEEDS'][0]['feed_last_read_iso']))
# print (json.dumps (scinfo['FEEDS'][1]['feed_last_read_iso']))
# print (json.dumps (scinfo['FEEDS'][0]['feed_previous_last_read_iso']))
#print (json.dumps (scinfo['FEEDS'][1]['feed_previous_last_read_iso']))


#reftimes =  flrtimes_unix
#reftimes = [now1,now2]
reftimes = [0,0]

leData = HolderFedFeed(feedData)
# leData.json()
# print (leData.feedQ)

# print (type(u_scinfo))

# print (leData.checknumfeeds(u_scinfo))

# print (leData.checknumfeeds_in())


leData.sort_entries()
leData.feedcounts()

# loop through the feeds to check against reftime, and if pubable,
# put into new unified raw queue


y = leData.feedQ

# print (leData.feeds)

for i in range (0, y):
    z = leData.counter[i]['numE']
    for j in range (0,z):
        lDe = leData.feeds[i][j]
        e = FedFeedEntry()
        # print (lDe)
        tf = e.checkEntry2Pub (lDe,reftimes[i])
        if tf == bool (True):
            # print (e.exgest())
            leData.newQueue(e.exgest())
            
        
toDoE = len (leData.UniFeed)
if toDoE < 1:
    print ('All done. Exiting')
    exit()
    
elif toDoE >= 1:
    keepgoing = bool(True)

else:
    print ('we are lost')
    exit()



midQueue = []


for i in range (0, toDoE):
    t = leData.newQueueExgest(i)
    a = entryCreate (t,i)
    # b is for blobs
    '''
    if blobcheck == True:
        b = blobadd (t)
        a.update (b)
    elif blobcheck != True:
        DoNothing = 1
    else:
        print ('We are lost')
    # Endf if
    '''
    midQueue.append (a)
    


print (json.dumps(midQueue))
exit()
# print ('\n\n\n')
# print (midQueue[0])


# need to chain in here adding images, sensitive    



# start working with bsky rubrick
count = len(midQueue)

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
# print (creds)


bpost = PostXwalk()

# bposts = [bpost] * count
sessT = Bcred.get_sessT()

myDID = Bcred.myDID()


# print (len(midQueue))
# for i in midQueue:
#     print (i)
    



for i in midQueue:
    
    bpost.addDID(myDID)
    mQe = i
    bpost.addText(mQe['basic_text'])
    bpost.addTime()
    
    BskyPosts.post_simple_ready (bpost,sessT)
# end loop

u_scinfo = StateConfigInfo.update_bsky_prev (u_scinfo)
uu_scinfo =  StateConfigInfo.update_bsky_now (u_scinfo)

j = StateConfigInfo.write_info(statecf, uu_scinfo)


