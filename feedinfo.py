"""
Feed info data structures
"""


feed_metadata = {
    'previous_last_read': 'unixtime',
    'last_read': 'unixtime',
    'number_elements':'integer 0-whatever',
    'oldest_post': 'unixtime',
    'youngest_post':'unixtime',
    'URL':'feed url string',
    'time_jitter': 'reserved'
}



post_constructor = {
    'original_url': 'long url from mastodon',
    'rating': 'reserved',
    'basic_text': 'string',
    'orig_post_time': 'convert to unixtime',
    'number_of_media': 'integer, 0-4 (hopefully)',
    'lang_of_post': 'string',
    'base_post_mime_t': 'string',
    'media_array': 'to be constructed'
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
    
    
