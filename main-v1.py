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


MainConfigInfo.create('moo.txt')

rval = StateConfigInfo.create('foo.toml')

t = MainConfigInfo.read('salt-main.toml')

x = StateConfigInfo.read('salt-state.toml')
x = StateConfigInfo.update_bsky_prev(x)
x = StateConfigInfo.update_bsky_now(x)
x = StateConfigInfo.update_bsky_prev(x)
x = StateConfigInfo.update_bsky_now(x)

z = StateConfigInfo.check_feed_nums(x)


hmf = FetchFeeds.check_feed_nums(t)


feedURLs = [0]* hmf
fd_content = [0]* hmf
feedURLs = FetchFeeds.find_feeds(t)

print (feedURLs)

for i in range (0,hmf):
    fd_content[i]= FetchFeeds.fetch_feed(feedURLs[i])
    FetchFeeds.sort_feed(fd_content[i])

print (fd_content)

exit ()





for i in range (0, numbo):
    j = FetchFeeds.enumerate_feed_items(feed[i])
    feed_items[i]=j

print(feed_items)

print (feed[0][0])

# sorted_feed = FetchFeeds.sort_feed(feed[0])

a = StateConfigInfo.write_info('salt-statetest.toml',x)
# print (x)
# print (y)
# print (x)
# print (x)


x = StateConfigInfo.update_feed_prev(x)
x = StateConfigInfo.update_feed_now(x)





# x = StateConfigInfo.update_feed_info(x)

# print (x)

exit()

configfileName = './salt-main.toml'

configDets = open_read_config(configfileName)
# Returns dict 'main_config': ,'state_config':
# print (configDets['main_config'])

# print ()

print (configDets['state_config'])
# print (configDets['main_config'])
'''
 


