''' docstring '''
# -*- mode: python; python-indent-offset: 4 -*-
import copy
import requests
import json
import time
# import ticktocktime
from ticktocktime import unix_time_now, bsky_time_now



class SimplePostQueue:
    ''' queue for simple bsky post '''
    def __init__(self,bsky_crd):
        self.s_p_queue = []
        self.rcode_list = []
        self.bsky_cred = bsky_crd
        self.API_URL = \
            'https://bsky.social/xrpc/com.atproto.repo.createRecord'
        self.p_template = {
            'repo': 'DID_credentials',
            'collection': 'app.bsky.feed.post',
            # 'rkey': 'string',
            'validate': True,
            'labels': [],
            'record': {
                'text' : 'text2post',
                'createdAt': 'now-time',
                '$type': 'app.bsky.feed.post',
                'langs': ['en'],
            }
        }
        self.h_template = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer <TOKEN>',
        }

    def item_craft (self, rawentry):
        ''' compose a simple bsky post '''
        URL = self.API_URL
        DID = self.bsky_cred['DID']
        ses_tok = self.bsky_cred['session_token']
        
        form_text = rawentry['basic_text_rev']
        text2post = form_text[0:298] # Blue sky limit is 300 char
        create_time = bsky_time_now()

        header_entry = self.h_template
        header_entry['Authorization'] = 'Bearer ' + ses_tok

        payload_entry = self.p_template
        payload_entry['repo'] = DID
        payload_entry['record']['text'] = text2post
        payload_entry['record']['createdAt'] = create_time
        

        # Change entry from tuple to dict or something
        entry = {
            'URL': URL ,
            'header_entry':header_entry,
            'payload_entry':payload_entry
            }
        insert = copy.deepcopy(entry)
        self.s_p_queue.append(insert)
        return insert

    def json_queue (self):
        print (json.dumps(self.s_p_queue))
        return

    def post_all_in_queue(self):
        for i in self.s_p_queue:
            p_1 =i.get('URL')
            p_2 =i.get('header_entry')
            p_3 =i.get('payload_entry')
            #print ('\n\n', p_3)
            rcode = post_the_post(p_1, p_2, p_3)
            self.rcode_list.append(rcode)
        # End For Loop
        return self.rcode_list


# End Class


# Start Functions

def post_the_post(URL,header_entry,payload_entry):
    payload = json.dumps (payload_entry)
    r = requests.post(URL,headers=header_entry,data=payload)
    print ()
    print ('*****************')
    print (payload)
    print ()
    
    if r.status_code != 200:
        print ("Status Code", r.status_code)
        print ("Message", r.text)
        raise Exception("Status code other than 200 indicates a problem")
    
    # implied else     elif r.status_code == 200:

    time.sleep(0.5) # sleep 0.5 seconds. test to see if rate limit issue
    print ("Status Code", r.status_code)
    print ("Message", r.text)
    return r


def PostXwalk():
    ''' dummy '''
    return


class BskyCredentials:
    def __init__(self):
        self.cred = credentials_dict
                                
    def printCred(self):
        print (self.cred)

    def _getHandle(self):
        return self.cred['handle']
    
    def set_handle(self, handle):
        self.cred['handle'] = handle

    def set_appPW(self,appPW):
        self.cred['app_pwd'] = appPW

    def echo(self):
        return self.cred
    
    def json (self):
        print (json.dumps(self.cred))
    
      
    def get_did(self):
      
        handle_header = {
            'Accept': 'application/json'
        }
        URLset = bskyURLdict
        URL = URLset.get('Get_DID_from_Handle')
        handle = self._getHandle()
        
        payload =  {'handle': handle}
        
        r = requests.get(URL, headers=handle_header, params=payload)
        
        if r.status_code != 200:
            print ("Status Code", r.status_code)
            print ("Message", r.text)
            raise Exception("Status code other than 200 indicates a problem")
        
        elif r.status_code == 200:
            roughdid = r.text
            jsondid = json.loads(roughdid)
            did = jsondid.get('did')
            self.cred['DID'] = did
        else:
            print ("we are lost")
            
        return self.cred['DID']

    def myDID (self):
        return self.cred['DID']
        
    def start_session(self):
        
        URL = bskyURLdict.get('Create_Session')

        content_info_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        prepayload = {
            'identifier':self.cred['DID'],
            'password': self.cred['app_pwd']
        }

        payload = json.dumps(prepayload)

        r = requests.post(URL, headers=content_info_header, data=payload)

        if r.status_code != 200:
            print ("Status Code", r.status_code)
            print ("Message", r.text)
            raise Exception("Status code other than 200 indicates a problem")
        
        elif r.status_code == 200:
            temp_i = json.loads (r.text)
            session_token = temp_i.get('accessJwt')
            refresh_token = temp_i.get('refreshJwt')
            tokens = {
                'session_token': session_token,
                'refresh_token': refresh_token
            }

        self.cred['session_token'] = tokens['session_token']
        self.cred['refresh_token'] = tokens['refresh_token']
        
        return self.cred
    
    def show_creds(self):
        return self.cred

    def get_sessT(self):
        return self.cred['session_token']

    def session_refresh(self):
        #stuff
        return 


credentials_dict = {
    'handle': 'static_text',
    'DID': 'static_text',
    'app_pwd': 'semi-static_text',
    'session_token': 'ephemeral',
    'refresh_token': 'ephemeral',
    'session_token_create_time': 'reserved',
    'refresh_token_create_time': 'reserved',
    'session_token_expiration': 'reserved',
    'refresh_token_expiration': 'reserved',

}

bskyURLdict = {
    'Get_DID_from_Handle'  : 'https://bsky.social/xrpc/com.atproto.identity.resolveHandle',
    'Create_Session' : 'https://bsky.social/xrpc/com.atproto.server.createSession',
    'Refresh_Session': 'https://bsky.social/xrpc/com.atproto.server.refreshSession',
    'Blob_Up' : 'https://bsky.social/xrpc/com.atproto.repo.uploadBlob',
    'Create_Record' : 'https://bsky.social/xrpc/com.atproto.repo.createRecord',
    'Get_Author_Feed' : 'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed',
    'Get_Actor_Feed': 'https://bsky.social/xrpc/app.bsky.feed.getActorFeeds',
    'Get_Home_Timeline':'https://bsky.social/xrpc/app.bsky.feed.getTimeline'
}
