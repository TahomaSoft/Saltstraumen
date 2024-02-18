"""
Feed info data structures
"""



'''
Data structure for main configuration elements
'''

simple_bsky_info = {
    'Username': 'A user Name',
    'App_passwd': 'a app password',
    'Nickname': 'account nickname'
}

main_config_genInfo = {
    'Title': 'Overall Config Name',
    'Statefile': 'name of the file to write state info',
    'TZ_abbr': 'UTC',
    'NumFeeds': 1
}

main_config_feedInfo = {
    'Name': 'Arbitrary Feed name for reference',
    'Number': 0,
    'URL': 'URL of the feed',
    'Type': 'rss',
    'TimeJitter': 0
}

state_config_genInfo = {
    'Title': 'a title'
}


feed_metadata = {
    'Name': 'Nick name for feed',
    'Number': 'item number',
    'URL':'feed url string',
    'feed_last_read_iso': 'iso time',
    'feed_last_read_unix': 'unixtime',
    'feed_previous_last_read_iso': 'iso time',
    'feed_previous_last_read_unix': 'unixtime',
    'newest_feed_item_unix':'unixtime',
    'newest_feed_item_iso':'iso time',
    'oldest_feed_item_iso': 'iso time',
    'oldest_feed_item_unix': 'unixtime',
}

bsky_post_metadata = {
    'previous_last_posted_unix':'unixtime',
    'previous_last_posted_iso': 'iso time',
    'last_posted_unix': 'unixtime',
    'last_posted_iso': 'iso time',
}

post_constructor = {
    'original_url': 'long url from mastodon',
    'rating': 'reserved',
    'html_text':'Original string from _summary_ ',
    'basic_text': 'string',
    'orig_post_time': 'convert to unixtime',
    'number_of_media': 'integer, 0-4 (hopefully)',
    'lang_of_post': 'string',
    'base_post_mime_t': 'string',
    'media_array': 'to be constructed from post_media_detail',
    'published_parsed': 'published parsed python',
    
}

post_media_detail = {
    'media_url': 'string',
    'media_type': 'mime-type-string',
    'media_size': 'filesize in bytes',
    'content_warn': 'content_warning if any',
    'content_rating':'adult, not adult, etc',
    'media_rating':'adult, not adult, etc',
    'sensitive_media': 'boolean, true or false',
    'alt_text': 'alt text string'
}
    
    
