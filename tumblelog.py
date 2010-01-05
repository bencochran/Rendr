'''

'''

from datetime import datetime
from time import mktime
import re, random

from blocks import match_block, filter_block
from htmltools import htmlspecialchars
from timetools import relative_time, GMT

post_types = {}

def post_type(type):
    '''
    Decorates a class and causes it to be the handler for a given type of post.
    '''
    def wrap_type(function):
        post_types[type] = function
        return function

    return wrap_type

def post_of_type(type):
    '''
    Returns the TumblelogPost associated with the given type.
    '''
    return post_types[type]

def post_is_type(post, typee):
    '''
    Check to see if a TumblelogPost instance is of the given type.
    '''
    return post_types.has_key(typee) and isinstance(post, post_types[typee])

def make_post(postData):
    '''
    Given a Tumblr-JSON-formatted dictionary of post data, create an instance 
    of the correct TumblelogPost subclass with the post data.
    '''
    postClass = post_of_type(postData['type'])
    return postClass(postData)


class Tumblelog(object):
    '''
    Basic tumblelog class. Takes a Tumblr-JSON-formatted dictionary of blog
    data and wraps it up into an object.  
    '''
    def __init__(self, data):
        self.title = data['tumblelog']['title']
        self.description = data['tumblelog']['description']
        
        if data['tumblelog']['cname']:
            self.url = 'http://%s' % data['tumblelog']['cname']
        else:
            self.url = 'http://%s.tumblr.com' % data['tumblelog']['name']
        
        self.posts = []
        for post in data['posts']:
            self.posts.append(make_post(post))

    def __getitem__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            raise IndexError
    
    def __str__(self):
        return 'Tumblelog: %(title)s, %(posts)s' % self    


class TumblelogPost(object):
    '''
    Tumblelog post class. Ingests a Tumblr-JSON-formatted dictionary. Also 
    handles rendering a post for a given template.
    '''
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url-with-slug']
        self.time = datetime.strptime(data['date-gmt'], '%Y-%m-%d %H:%M:%S %Z')
        self.format = data['format']
        self.tags = data['tags'] if data.has_key('tags') else []
        
        def sanitize_tag(tag):
            return re.sub('\W', '_', tag)
        
        self.tagsAsClasses = " ".join(re.sub('\W', '_', tag)
            for tag in self.tags)
        
        self.notes = []
        for i in range(random.randint(0,10)):
            self.notes.append('hello')

    def __getitem__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            raise IndexError
    
    def __str__(self):
        return '%(__class__)s: #%(id)s %(url)s' % (self)
    
    def render(self, template):
        def singplural(singular, plural, c):
            if c == 1: return singular
            else: return plural
        
        ignored_blocks = ['More']

        ignored_tags = ['PostNotes', 'ReblogParentName', 'ReblogParentTitle',\
            'ReblogParentURL', 'ReblogParentPortraitURL-16',\
            'ReblogParentPortraitURL-24', 'ReblogParentPortraitURL-30',\
            'ReblogParentPortraitURL-40', 'ReblogParentPortraitURL-48',\
            'ReblogParentPortraitURL-64', 'ReblogParentPortraitURL-96',\
            'ReblogParentPortraitURL-128', 'ReblogRootName',\
            'ReblogRootTitle', 'ReblogRootURL', 'ReblogRootPortraitURL-16',\
            'ReblogRootPortraitURL-24', 'ReblogRootPortraitURL-30',\
            'ReblogRootPortraitURL-40', 'ReblogRootPortraitURL-48',\
            'ReblogRootPortraitURL-64', 'ReblogRootPortraitURL-96',\
            'ReblogRootPortraitURL-128'\
        ]
        
        template = filter_block('HasTags', len(self.tags) > 0, template)
        template = filter_block('NoteCount', len(self.notes) > 0, template)
        
        for block in ignored_blocks:
            template = filter_block(block, False, template)
        
        for tag in ignored_tags:
            template = template.replace('{%s}' % tag, '')
        
                
        template = template.replace('{Permalink}', self.url)
        template = template.replace('{PostID}', '%s' % self.id)
        template = template.replace('{TimeAgo}', relative_time(self.time,
            datetime.utcnow()))
        template = template.replace('{DayOfMonth}', '%d' % self.time.day)
        template = template.replace('{DayOfMonthWithZero}',
            '%02d' % self.time.day)
        template = template.replace('{DayOfWeek}', self.time.strftime('%A'))
        template = template.replace('{ShortDayOfWeek}', 
            self.time.strftime('%a'))
            
        template = template.replace('{DayOfWeekNumber}', 
            '%s' % self.time.isoweekday())
        
        # http://mail.python.org/pipermail/python-list/2005-July/333218.html
        template = template.replace('{DayOfMonthSuffix}', 
            "th" if 4 <= self.time.day <= 20 or 24 <= self.time.day <= 30 \
            else ["st", "nd", "rd"][self.time.day % 10 - 1])
            
        
        template = template.replace('{DayOfYear}', 
            self.time.strftime('%j').lstrip('0'))
        template = template.replace('{WeekOfYear}', 
            '%s' % (int(self.time.strftime('%U')) + 1))
        
        template = template.replace('{Month}', self.time.strftime('%B'))
        template = template.replace('{ShortMonth}', self.time.strftime('%b'))
        template = template.replace('{MonthNumber}', 
            self.time.strftime('%m').lstrip('0'))
        template = template.replace('{MonthNumberWithZero}', 
            self.time.strftime('%m'))
        template = template.replace('{Year}', self.time.strftime('%Y'))
        template = template.replace('{ShortYear}', self.time.strftime('%y'))
        template = template.replace('{AmPm}', self.time.strftime('%p').lower())
        template = template.replace('{CapitalAmPm}', self.time.strftime('%p'))
        template = template.replace('{12Hour}', 
            self.time.strftime('%I').lstrip('0'))
        template = template.replace('{24Hour}', 
            self.time.strftime('%J').lstrip('0'))
        template = template.replace('{12HourWithZero}', 
            self.time.strftime('%I'))
        template = template.replace('{24HourWithZero}', 
            self.time.strftime('%J'))
        template = template.replace('{Minutes}', self.time.strftime('%M'))
        template = template.replace('{Seconds}', self.time.strftime('%S'))
        template = template.replace('{Beats}', '')
        template = template.replace('{Timestamp}', 
            '%s' % mktime(self.time.timetuple()))
        template = template.replace('{NoteCountWithLabel}', '%d %s' %
            (len(self.notes), singplural('note', 'notes', len(self.notes))))
        template = template.replace('{TagsAsClasses}', self.tagsAsClasses)
        
        @match_block('Tags')
        def render_tags(template):
            content = u''
            for tag in self.tags:
                tagmarkup = template.replace('{Tag}', tag)
                tagmarkup = tagmarkup.replace('{TagURL}', '/tagged/%s' % tag)
                content = content + tagmarkup
            return content
        
        template = render_tags(template)
        
        return template

@post_type('text')
@post_type('regular')
@post_type('Text')
class TextPost(TumblelogPost):
    def __init__(self, data):
        super(TextPost, self).__init__(data)
        self.title = data['regular-title']
        self.body = data['regular-body']
    
    def render(self, template):
        template = super(TextPost, self).render(template)

        template = filter_block('Title', self.title, template)
        template = filter_block('More', True, template)
        template = template.replace('{Title}', self.title)
        template = template.replace('{Body}',self.body)
        
        return template

@post_type('photo')
@post_type('Photo')
class PhotoPost(TumblelogPost):
    def __init__(self, data):
        super(PhotoPost, self).__init__(data)
        self.caption = data['photo-caption']
        self.link = data['photo-link-url'] if data.has_key('photo-link-url') else None
        self.photo = {
            '1280' : data['photo-url-1280'],
            '500' : data['photo-url-500'],
            '400' : data['photo-url-400'],
            '250' : data['photo-url-250'],
            '100' : data['photo-url-100'],
            '75' : data['photo-url-75']
        }
    
    def has_highres(self):
        return not self.photo['1280'] == self.photo['500']
    
    def render(self, template):
        template = super(PhotoPost, self).render(template)        
        
        template = filter_block('Caption', self.caption, template)
        template = filter_block('HighRes', self.has_highres(), template)
        template = template.replace('{Caption}',self.caption)
        template = template.replace('{LinkOpenTag}', '<a href={LinkURL}>' if 
            self.link else '')
        template = template.replace('{LinkCloseTag}', '</a>' if 
            self.link else '')
        template = template.replace('{LinkURL}',self.link if self.link else '')
        
        template = template.replace('{PhotoURL-500}', self.photo['500'])
        template = template.replace('{PhotoURL-400}', self.photo['400'])
        template = template.replace('{PhotoURL-250}', self.photo['250'])
        template = template.replace('{PhotoURL-100}', self.photo['100'])
        template = template.replace('{PhotoURL-75sq}', self.photo['75'])
        
        template = template.replace('{PhotoURL-HighRes}', self.photo['1280'])


        return template
        

@post_type('photoset')
@post_type('Photoset')
class PhotosetPost(TumblelogPost):
    def __init__(self, data):
        super(PhotosetPost, self).__init__(data)

@post_type('quote')
@post_type('Quote')
class QuotePost(TumblelogPost):
    def __init__(self, data):
        super(QuotePost, self).__init__(data)
        self.text = data['quote-text']
        self.source = data['quote-source']

    def render(self, template):
        template = super(QuotePost, self).render(template)        

        template = filter_block('Source', self.source, template)
        template = template.replace('{Quote}',self.text)
        template = template.replace('{Source}',self.source)
        # Length?
        
        return template


@post_type('link')
@post_type('Link')
class LinkPost(TumblelogPost):
    def __init__(self, data):
        super(LinkPost, self).__init__(data)
        self.text = data['link-text']
        self.link_url = data['link-url']
        self.description = data['link-description']

    def render(self, template):
        template = super(LinkPost, self).render(template)        

        template = filter_block('Description', self.description, template)
        template = template.replace('{URL}', self.link_url)
        template = template.replace('{Name}', self.text)
        template = template.replace('{Target}', 'target="_blank"')
        template = template.replace('{Description}', self.description)
        
        return template

        
@post_type('conversation')
@post_type('Conversation')
@post_type('Chat')
class ConversationPost(TumblelogPost):
    def __init__(self, data):
        super(ConversationPost, self).__init__(data)
        
@post_type('audio')
@post_type('Audio')
class AudioPost(TumblelogPost):
    def __init__(self, data):
        super(AudioPost, self).__init__(data)
        self.caption = data['audio-caption']
        self.player = data['audio-player']
        self.plays = int(data['audio-plays'])

    def player_color(self, color):
        return self.player.replace('color=FFFFFF', 'color=%s' % color)

    def formatted_plays(self):
        return '%s' % self.plays

    def render(self, template):
        template = super(AudioPost, self).render(template)        

        template = filter_block('Caption', self.caption, template)
        template = filter_block('ExternalAudio', False, template)
        template = template.replace('{Caption}', self.caption)
        template = template.replace('{AudioPlayer}', self.player)
        template = template.replace('{AudioPlayerWhite}',
            self.player_color('FFFFFF'))
        template = template.replace('{AudioPlayerGrey}',
            self.player_color('E4E4E4'))
        template = template.replace('{AudioPlayerBlack}',
            self.player_color('000000'))
        template = template.replace('{PlayCount}', '%s' % self.plays)
        template = template.replace('{FormattedPlayCount}', 
            self.formatted_plays())
        template = template.replace('{ExternalAudioURL}', '#')
        
        return template

    
@post_type('video')
@post_type('Video')
class VideoPost(TumblelogPost):
    def __init__(self, data):
        super(VideoPost, self).__init__(data)
        self.caption = data['video-caption']
        self.player = data['video-player']
        self.source = data['video-source']
