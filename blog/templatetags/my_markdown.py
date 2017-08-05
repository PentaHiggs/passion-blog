from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import markdown

register = template.Library()

@register.filter(
        name='process_markdown',
        needs_autoescape=True,
        #is_safe=False,               # Needed so the html is not messed with.            
        )
def process_markdown(text, style, autoescape=True):
    """Processes markdown in the given text

    Uses pygments on any encountered code blocks
    """

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    
    style = "friendly"

    # Don't need to escape text, text is automatically escaped by markdown
    ret_string = markdown.markdown( text,
                                    extensions=['markdown.extensions.codehilite'],
                                    extension_configs = {
                                        'markdown.extensions.codehilite' : {
                                            'linenums'      : False,
                                            'pygments_style': style,
                                            }
                                        }
                                    )

    return mark_safe(ret_string)

