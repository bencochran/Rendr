import re

def htmlspecialchars(string):
    '''
    Simple copy of PHP's htmlspecialchars
    '''
    return string.replace('&', '&amp;').replace('"', '&quot;')\
        .replace("'", '&#039;').replace('<', '&lt;').replace('>', '&gt;')

def urlsafe(string):
    return re.sub('\W', '_', string)