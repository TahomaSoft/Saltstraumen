#!/usr/bin/python3

import toml
import time
from datetime import date, datetime, timezone
from configswork import readMainConfig, readStateConfig, writeStateConfig
import feedparser

# this is the main program

configfile_name = './salt-main.toml'
statefile_name = './salt-state.toml'

# Open the main and state config files, read, get data, and close the files
main_config = readMainConfig(configfile_name)
state_config = readStateConfig(statefile_name)

# now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
# now_iso = datetime.now(timezone.utc).isoformat()
now_unix = time.time()

print (now_unix)
lastread_iso = state_config['FEED_1']['feed_last_read']

print (lastread_iso)

lastread_unix = time.strptime(lastread_iso, "%Y-%m-%dT%H:%M:%S.%f%z")
print (lastread_unix)
# lastreadiso = lastreadz.replace("Z", "+00:00")
# lastreadparse = datetime.fromisoformat(lastreadiso)



# state_config['FEED_1']['feed_last_read'] = now_iso
state_config['FEED_1']['URL'] = main_config['FEED_1']['URL']
feed1_url  = main_config['FEED_1']['URL']

feed1 = feedparser.parse(feed1_url)


items_retrieved = len(feed1['entries'])
entries_retrieved = feed1['entries']
most_recent = entries_retrieved[0]

print (most_recent)
python_time = most_recent['published_parsed']
s = python_time
print (python_time)
print (type(python_time))

# print (python_time.isoformat())

dt = datetime(*s[:6], tzinfo=timezone.utc) # iterated unpacking


# print (now_iso.timetuple())

# happytime = datetime(python_time).isoformat()

# print (happytime)

       


# Open, update, and close state file

writeStateConfig(statefile_name,state_config)

    




