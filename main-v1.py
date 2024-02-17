#!/usr/bin/python

"""
Goal for this test module is to pull in one post from mastodon and
repost it on bluesky.
"""
from SaxeBlueskyPython import ticktocktime
import feedstructs
from  heavy_lifting import open_read_config





configfileName = './salt-main.toml'

configDets = open_read_config(configfileName)
# Returns dict 'main_config': ,'state_config':
# print (configDets['main_config'])

# print ()

#print (configDets['state_config'])
print (configDets['main_config'])


exit()
