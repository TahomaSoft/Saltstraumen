#!/usr/bin/python3

import toml
from datetime import date, datetime, time, timezone

mainconfigfile_name = './salt-main.config'
with open(mainconfigfile_name, 'r') as mainconfigfile:
    toml_in = toml.load(mainconfigfile)

# print (toml_in)

outfile_name = './salt-main.toml'

with open(outfile_name, 'w') as outfile:
    toml.dump(toml_in, outfile)


stateconfigfile_name = './salt-state.config'
with open (stateconfigfile_name, 'r') as stateconfigfile:
    statetoml_in = toml.load(stateconfigfile)

now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

statetoml_in['FEED_1']['feed_last_read'] = now_iso
statetoml_in['FEED_1']['URL']= toml_in['FEED_1']['URL']
stateoutfile_name = './salt-state.toml'

with open(stateoutfile_name, 'w') as stateoutfile:
    toml.dump(statetoml_in, stateoutfile)

