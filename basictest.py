#!/usr/bin/python3
import copy
import json
from config_feed_objsmeth import MainConfigInfo, StateConfigInfo,chk_main_state
from config_feed_objsmeth import fetch_feed #, enumerate_feed_items
from FediQueueObjects import FirstFediQueue
from FediXbSky import BasicBlueskyQueue
# from saxe_bluesky import 
from saxeblueobjects import SimplePostQueue, BskyCredentials
from ticktocktime import unix_time_now, bsky_time_now

# this is the main program

configfile_name = './salt-main.toml'
statefile_name = './salt-state.toml'

# Open the main and state config files, read, get data, and close the files
# proper handling of time formats will be needed.

# Maybe right approach to time is keeping all the stuff in the saxe
# blue library in the time format that bluesky expects, keep
# everything here in unix time, and convert as needed.


# MainConfigInfo.create ('salt-main.toml', 2)

main_config =  MainConfigInfo(configfile_name)
main_config.read()
q = main_config.state_fname()


# StateConfigInfo.create (q, 2)
state_config = StateConfigInfo(q)
state_config.read()
# state_config.print()



state_config.check_feed_num()
main_config.check_feed_num()
# main_config.write()
# print (state_config.update_feed_prev())
state_config.add_URLs(main_config.show_feeds())
state_config.update_feed_now()
state_config.update_bsky_prev()
state_config.update_bsky_now()
# state_config.print()
state_config.write_state()

feedData = []

for i in state_config.show_feeds():
    # print(i)
    feedData.append(fetch_feed(i))

fqueue_1 = FirstFediQueue (feedData)
# fqueue_1.print()
ef = fqueue_1.enumerate_feeds()
#fqueue_1.enumerate_feed_items()
# print (len (fqueue_1.feeds[0]))
# print (len (fqueue_1.feeds[1]))



j = fqueue_1.enumerate_feed_items()
    
fqueue_1.sort_entries()

#fqueue_1.print_feeds()
# fqueue_1.json_sorted_feeds()


state_config.update_entry_times(fqueue_1.sorted_feeds,j)



#reftimes = state_config.get_ref_times()
reftimes = (2222,222) # for testing


state_config.write_state()


fqueue_1.mark_entries4pub(reftimes)

# fqueue_1.json_marked_queue()

'''
for i in fqueue_1.marked_feed_entries2pub:
    print ()
    print ('*******************')
    print (json.dumps(i))
    print ()
'''

# BasicBlueskyQueue(fqueue_1.marked_feed_entries2pub)

Bsky_1 = BasicBlueskyQueue(fqueue_1.marked_feed_entries2pub)

Bsky_1.first_clean()
# Bsky_1.json_firstpassq()


Bcred = BskyCredentials()

# print (mcfdata['BSKY_ACCOUNT'])
acct_name =main_config.config_data['BSKY_ACCOUNT']['Username']


Bcred.set_handle (acct_name)



appPass = main_config.config_data['BSKY_ACCOUNT']['App_passwd']

Bcred.get_did ()
Bcred.set_appPW (appPass)
Bcred.start_session()
sessT = Bcred.get_sessT()
# print (sessT)
myDID = Bcred.myDID()

spq = SimplePostQueue(Bcred.echo())

jj= Bsky_1.queue_sze()

tt = len (Bsky_1.first_pass_queue)



for i in range (0,jj):  # skip first element because init with [{}]
    item =''
    item = Bsky_1.queue_itm_exgest(i)
    #print()
    #print ('*****~~~~~******')
    #print (item)
    #print ()
    #print ('^^^^^^^^^^^')
    mod_item = copy.deepcopy(spq.item_craft(item))
    #print (mod_item)
    #print ('~~~~~~~~~~~~')
    #temp_q.append (mod_item)

#spq.json_queue()

# spq.post_all_in_queue()
