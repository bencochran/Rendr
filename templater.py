'''
The Tumblr templater. Handles rendering a template for a Tumblelog object.
'''

from blocks import match_block, filter_block
from tumblelog import post_is_type
from htmltools import htmlspecialchars
from timetools import sameday

def render_single_post(post, template):
    types = ['Regular', 'Text', 'Photo', 'Photoset', 'Quote', 'Link', 
        'Conversation', 'Chat', 'Audio', 'Video']
    
    # Filter out the post block to only contain the relevant stuff
    for type in types:
        # print type, post_is_type(post, type)
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

    template = render_posts(template)
    template = filter_block('SearchPage', False, template)
    template = filter_block('PostSummary', False, template)
    template = filter_block('Description', blog.description, template)
    template = filter_block('NextPage', False, template)
    template = filter_block('PreviousPage', True, template)
    template = filter_block('PermalinkPage', False, template)
    template = filter_block('IndexPage', True, template)
    template = filter_block('PostTitle', False, template)
    template = filter_block('PostSummary', False, template)
    template = filter_block('Pagination', True, template)
    template = filter_block('PermalinkPagination', False, template)
    template = filter_block('PreviousPost', False, template)
    template = filter_block('NextPost', False, template)
    
    template = template.replace('{Title}', blog.title)
    template = template.replace('{Description}', blog.description)
    template = template.replace('{MetaDescription}',
        htmlspecialchars(blog.description))
    template = template.replace('{RSS}', '%s/rss' % blog.url)
    template = template.replace('{PreviousPage}', '%s/page/2' % blog.url)
    template = template.replace('{NextPage}', '')
    template = template.replace('{CurrentPage}', '1')
    template = template.replace('{TotalPages}', '15')
    template = template.replace('{PostTitle}', '')
    template = template.replace('{PostSummary}', '')
    template = template.replace('{PreviousPost}', '')
    template = template.replace('{NextPost}', '')
    template = template.replace('{Favicon}', '')
    template = template.replace('{CustomCSS}', '')

    return template
