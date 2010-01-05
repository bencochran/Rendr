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
        for post in blog.posts:
            content = content + render_single_post(post, template)
        return content

    template = render_posts(template)
    template = filter_block('SearchPage', False, template)
    template = filter_block('PostSummary', False, template)
    template = filter_block('Description', blog.description, template)
    template = filter_block('NextPage', False, template)
    template = filter_block('PreviousPage', True, template)
    
    template = template.replace('{Title}', blog.title)
    template = template.replace('{Description}', blog.description)
    
    return template
