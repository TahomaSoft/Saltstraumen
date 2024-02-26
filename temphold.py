def entryAddRatings (rawpost):
    #  These elements are conditional; need to check and handle absent/present'''
    e = rawpost
    MRat = {}

    r = {'rating': ''}
    
    mr = {'media_rating':''}
    
    t = {'tags':''}

    ft = {'fixed_tags':''}
        
    
    if e.get('media_rating') != None:
        mr['media_rating'] = e['media_rating']['content']
        MRat.append(mr)
        
    elif e.get('media_rating') == None:
        mr = ['media_rating'] = 'nonadult'
        MRat.append(mr)
         
    if e.get('rating') != None:
        r['rating'] = e['rating']
        MRat.append (r)       
    elif e.get('rating') == None:
        r['rating'] = 'nonadult'
        MRat.append (r)
    if e.get('tags') == None:
        ft['fixed_tags'] == None
        MRat.append (ft)
    elif e.get('tags') != None:
        t['tags'] = e['tags']
        MRat.append(t)
        j = e['tags']
        #ft['fixed_tags'] = entryFixTags(j)
    else:
        print ('we are lost')
       
     
    return MRat

def addSummaryDetail(rawpost):

    e = rawpost
    
    aSD = {}

    f = {
        'summary_detail': '',
        'base_post_mime_t':
        'alt_lang_post':
        'base_url':
        'html_text_sdetail'
        }
        
    # Get Summary detail
    if 'summary_detail' in e.keys():
        sd = e['summary_detail']
        f['base_post_mime_t'] = sd['type']
        f['alt_lang_post'] = sd['language']
        f['base_url'] = sd['base']
        f['html_text_sdetail'] = sd['value']
    # end if

    aSD.update (f)
    return aSD


def something

    
    # check for content warning in original html_text
    txtCWtpl = cw_check (origTxt)
    contentWarn = txtCWtpl[0]
    cleanMainTxt = txtCWtpl[1]
    f['content_warn'] = contentWarn
    f['contentWarn'] = contentWarn
    f['basic_text_rev'] = cleanMainTxt
    return f


