#!/usr/bin/python3

import toml
import time
from datetime import date, datetime, timezone

mainconfigfile_name = './salt-main.toml'
with open(mainconfigfile_name, 'r') as mainconfigfile:
    toml_in = toml.load(mainconfigfile)
    mainconfigfile.close


stateconfigfile_name = './salt-state.toml'
with open (stateconfigfile_name, 'r') as stateconfigfile:
    statetoml_in = toml.load(stateconfigfile)
    stateconfigfile.close()

statetoml_in['FEED_1']['feed_previous_last_read_unix'] \
    = statetoml_in['FEED_1']['feed_last_read_unix']
statetoml_in['FEED_1']['feed_previous_last_read_iso'] = \
     statetoml_in['FEED_1']['feed_last_read_iso']

# now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
now_iso = datetime.now(timezone.utc).isoformat()
now_unix = time.time()

statetoml_in['FEED_1']['feed_last_read_unix'] = now_unix
statetoml_in['FEED_1']['feed_last_read_iso'] = now_iso
statetoml_in['FEED_1']['URL']= toml_in['FEED_1']['URL']

stateoutfile_name = './salt-state.toml'

with open(stateoutfile_name, 'w') as stateoutfile:
    toml.dump(statetoml_in, stateoutfile)
    stateoutfile.close()
