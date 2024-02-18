#!/usr/bin/python

"""
Goal for this test module is to pull in one post from mastodon and
repost it on bluesky.
"""
# import syslog
from SaxeBlueskyPython import ticktocktime
import feedstructs
from  heavy_lifting import MainConfigInfo, StateConfigInfo, FetchFeeds
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

print (z)

# exit()

hmf = MainConfigInfo.check_feed_nums(t)


feedURLs = [0]*hmf
full_fd_content = [0]*hmf
ent_fd  = [0]*hmf
entries_per_feed =  [0]*hmf
uet = [0,0]*hmf # updated entry times
j = entries_per_feed
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

uet=StateConfigInfo.update_entry_times (ent_fd,x)

# print (json.dumps(uet))

x = StateConfigInfo.write_info('salt-state.toml',uet)
exit ()


