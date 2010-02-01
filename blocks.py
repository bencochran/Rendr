import re

def filter_block(block, boolean, template):
    '''
    If boolean is false remove the block from the template, otherwise keep the
    block (without the block tags).
    '''
    @match_block(block)
    def matcher(template):
        if boolean: return template
        else: return ''
    
    return matcher(template)

def match_block(block):
    '''
    Decorator for block renderers. This allows a much nicer system for 
    rendering blocks. It handles the regular expression creation and 
    substitution, allowing you to simply write function to render. Use it as
    follows:
    
        @match_block('Title')
        def render_title(template):
            return template.replace('{Title}', 'Hello!')
        
        template = '{block:Title}Title: {Title}{/block:Title}'
        print render_title(template)
    
    This would simply print 'Title: Hello!'
    '''
    def wrap_matcher(function):
        def wrap_function(template):            
            def call_function(match):
                template = match.group(1)
                return function(template)
            # The optional / on the closing tag shouldn't be optional. But
            # some theme designers seem to leave it out and Tumblr is happy
            # to oblige. Since I'm trying to mimic Tumblr.. I'll also mimic
            # their mistakes.
            return re.sub(r'(?s){block:%s}(.*?){/?block:%s}' % (block, block), call_function, template)
        return wrap_function
    return wrap_matcher