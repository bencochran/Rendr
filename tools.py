from datetime import datetime, timedelta, tzinfo

def load_stream(stream):
    '''
    Given a stream (like a file or open url), read contents to the end and
    return them. Warning: only use this if you know your stream has an end or
    if you like programs that do nothing for a while. Like until you kill them.
    '''
    contents = u''
    
    while True:
        chunk = stream.read()
        contents = contents + chunk.decode('utf8')
        
        if chunk == '':
            break
    
    return contents

def relative_time(d, now=None):
    '''
    Give the relative time since the post's creation time. Will return 
    something like '4 hours ago' or '1 week ago'

    Adapted from: http://code.djangoproject.com/browser/django/trunk/django/utils/timesince.py
    
    '''
    def singplural(singular, plural, c):
        if c == 1: return singular
        else: return plural
    
    chunks = (\
        (60 * 60 * 24 * 365, lambda n: singplural('year', 'years', n)),\
        (60 * 60 * 24 * 30, lambda n: singplural('month', 'months', n)),\
        (60 * 60 * 24 * 7, lambda n : singplural('week', 'weeks', n)),\
        (60 * 60 * 24, lambda n : singplural('day', 'days', n)),\
        (60 * 60, lambda n: singplural('hour', 'hours', n)),\
        (60, lambda n: singplural('minute', 'minutes', n))\
    )
    
    if d and not isinstance(d,datetime):
        now = datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime):
        now = datetime(now.year, now.month, now.day)
    if not now:
        if d.tzinfo:
            now = datetime.now(d.tzinfo)
        else:
            now = datetime.now()

    delta = now - (d - timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds

    if since <= 0:
        return u'just now'

    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = '%(number)d %(type)s ago' % {'number': count, 'type':name(count)}
    return s

def sameday(d1, d2):
    '''
    True if d1 and d2 represent the same day, False if not
    '''
    if not isinstance(d1, datetime) or \
        not isinstance(d2, datetime): return False
    
    return d1.year == d2.year and d1.month == d2.month and d1.day == d2.day
