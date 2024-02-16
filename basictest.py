#!/usr/bin/python3
import calendar
import toml
import time
from operator import attrgetter
from datetime import date, datetime, timezone
from configswork import readMainConfig, readStateConfig, writeStateConfig
import feedparser

# this is the main program

configfile_name = './salt-main.toml'
statefile_name = './salt-state.toml'

# Open the main and state config files, read, get data, and close the files
# proper handling of time formats will be needed.

# Maybe right approach to time is keeping all the stuff in the saxe
# blue library in the time format that bluesky expects, keep
# everything here in unix time, and convert as needed.


main_config = readMainConfig(configfile_name)
state_config = readStateConfig(statefile_name)


now_unix = time.time()
now_iso  = datetime.now(timezone.utc).isoformat()
lastread_iso = state_config['FEED_1']['feed_last_read_iso']
lastread_unix = time.strptime(lastread_iso, "%Y-%m-%dT%H:%M:%S.%f%z")
# lastread_unix = time.strptime(lastread_iso, "%Y-%m-%dT%H:%M:%S.%f%z")


# state_config['FEED_1']['feed_last_read'] = now_iso
state_config['FEED_1']['URL'] = main_config['FEED_1']['URL']
feed1_url  = main_config['FEED_1']['URL']

feed1 = feedparser.parse(feed1_url)


items_retrieved = len(feed1['entries'])
entries_retrieved = feed1['entries']

print ("Items Retrieved: \n", items_retrieved)
# print ("Entries Retrieved: \n", entries_retrieved)

sorted_entries = sorted(entries_retrieved, reverse = True, key=attrgetter('published_parsed'))

most_recent = entries_retrieved[0]
oldest = entries_retrieved[items_retrieved-1]

print ('Most Recent \n')
print (most_recent)
python_time = most_recent['published_parsed']
s = python_time
print (s)
print (type(s))

print ('Oldest \n')

print (oldest)


# print (python_time.isoformat())

dt = datetime(*s[:6], tzinfo=timezone.utc) # iterated unpacking
print (dt)

rtime = calendar.timegm(s)
print (rtime)

state_config['FEED_1']['newest_feed_item_unix'] = rtime

# print (now_iso.timetuple())

# happytime = datetime(python_time).isoformat()

# print (happytime)

       


# Open, update, and close state file

writeStateConfig(statefile_name,state_config)

    




