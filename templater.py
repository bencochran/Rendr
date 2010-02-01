'''
The Tumblr templater. Handles rendering a template for a Tumblelog object.
'''
import re

from blocks import match_block, filter_block
from tumblelog import post_is_type
from htmltools import htmlspecialchars, striptags
from timetools import sameday

def load_meta_tags(template):
    '''
    Find custom meta tags and build up the proper tag and block information for
    them. Returns a tuple of (tags, blocks) where 'tags' is a list of (name, 
    value) tuples and 'blocks' is a list of (block_name, boolean) tuples.
    '''
    tags = []
    blocks = []
    
    def findAttr(attr, tag):
        '''
        Given an HTML tag, find the value of an attribute.
        '''
        matches = re.search(r'(?s)%s\s*=\s*([\'"])(.*?)\1' % attr, tag)
        return matches.group(2) if matches else None
    
    matches = re.finditer(r'(?s)<meta\b.*?>', template)
    
    for match in matches:
        tag = match.group(0)

        name = findAttr('name', tag)
        content = findAttr('content', tag)

        # Skip meta tags without a name
        if not name: continue

        # Convert to proper camel case
        fullName = re.sub(r'\s+(\w)', lambda m: m.group(1).upper(), name)

        try:
            (nameType, name) = fullName.split(':')
        except ValueError:
            # Skip improperly formatted names
            continue
        
        if nameType == 'if':
            content = ('content' == '1')

            blocks.append(('If%s' % name, content))
            blocks.append(('IfNot%s' % name, not content))
        else:
            if nameType == 'image':
                blockName = '%sImage' % name
            else:
                blockName = name
            
            # If it has content then the it's block is True
            blockContent = True if content else False

            blocks.append(('If%s' % blockName, blockContent))        
            blocks.append(('IfNot%s' % blockName, not blockContent))        
            tags.append((fullName, content))
    return (tags, blocks)

def render_single_post(post, template):
    types = ['Regular', 'Text', 'Photo', 'Photoset', 'Quote', 'Link', 
        'Conversation', 'Chat', 'Audio', 'Video', 'Answer']
    
    # Filter out the post block to only contain the relevant stuff
    for type in types:
        template = filter_block(type, post_is_type(post, type), template)

    template = post.render(template)

    return template
        
def render(blog, template):
    '''
    Renders a blog with the given template.
    '''
    
    @match_block('Posts')
    def render_posts(template):
        content = u''
        previousDay = None
        for i, post in enumerate(blog.posts):
            template = filter_block('NewDayDate',
                not sameday(previousDay, post.time), template)
            template = filter_block('SameDayDate',
                sameday(previousDay, post.time), template)
            template = filter_block('Odd', not i % 2, template)
            template = filter_block('Even', i % 2, template)
            content = content + render_single_post(post, template)
        return content

    # Load in all the custom stuff
    (customTags, customBlocks) = load_meta_tags(template)

    # First, render posts.
    template = render_posts(template)


    ignored_blocks = ['SearchPage', 'PostSummary', 'NextPage', \
        'PermalinkPage', 'PostTitle', 'PostSummary', 'PermalinkPagination', \
        'PreviousPost', 'NextPost', 'GroupMembers', 'GroupMember', 'DayPage', \
        'DayPagination', 'PreviousDayPage', 'NextDayPage', 'TagPage', \
        'SearchPage', 'NoSearchResults', 'Following', 'Followed', 'Likes', \
        'PostNotes']
    
    ignored_tags = ['NextPage', 'PostTitle', 'PostSummary', 'PreviousPost', \
        'NextPage', 'Favicon', 'CustomCSS', 'GroupMemberName', \
        'GroupMemberTitle', 'GroupMemberURL', 'GroupMemberPortraitURL-16', \
        'GroupMemberPortraitURL-24', 'GroupMemberPortraitURL-30', \
        'GroupMemberPortraitURL-40', 'GroupMemberPortraitURL-48', \
        'GroupMemberPortraitURL-64', 'GroupMemberPortraitURL-96', \
        'GroupMemberPortraitURL-128', 'PreviousDayPage', 'NextDayPage', 'Tag',\
        'URLSafeTag', 'TagURL', 'TagURLChrono', 'SearchQuery', \
        'URLSaveSearchQuery', 'SearchResultCount', 'FollowedName', \
        'FollowedTitle', 'FollowedURL', 'FollowedPortraitURL-16', \
        'FollowedPortraitURL-20', 'FollowedPortraitURL-30', \
        'FollowedPortraitURL-40', 'FollowedPortraitURL-48', \
        'FollowedPortraitURL-64', 'FollowedPortraitURL-96', \
        'FollowedPortraitURL-128', 'Likes']

    for block in ignored_blocks:
        template = filter_block(block, False, template)
    
    for tag in ignored_tags:
        template = template.replace('{%s}' % tag, '')

    for (block, shouldFilter) in customBlocks:
        template = filter_block(block, shouldFilter, template)

    for (tag, value) in customTags:
        template = template.replace('{%s}' % tag, value)

    template = filter_block('Description', blog.description, template)
    template = filter_block('PreviousPage', True, template)
    template = filter_block('IndexPage', True, template)
    template = filter_block('Pagination', True, template)
    
    template = filter_block('Twitter', blog.twitterUsername, template)
    template = template.replace('{TwitterUsername}', blog.twitterUsername)
    
    template = template.replace('{Title}', blog.title)
    template = template.replace('{Description}', blog.description)
    template = template.replace('{MetaDescription}', 
        striptags(blog.description))
    template = template.replace('{RSS}', '%s/rss' % blog.url)
    template = template.replace('{PreviousPage}', '%s/page/2' % blog.url)
    template = template.replace('{CurrentPage}', '1')
    template = template.replace('{TotalPages}', '15')

    template = re.sub('{Likes limit="\d+"}', '', template)
    template = re.sub('{Likes width="\d+"}', '', template)
    template = re.sub('{Likes summarize="\d+"}', '', template)

    return template
