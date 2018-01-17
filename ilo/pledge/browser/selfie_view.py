from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.selfie import ISelfie

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ISelfie)
    grok.require('zope2.View')
    grok.template('selfie_view')
    grok.name('view')
    
    def text_direction_value(self):
        parent = self.context.aq_parent
        value = 'ltr'
        if hasattr(parent, 'text_direction'):
            if parent.text_direction:
                value = parent.text_direction
        return value

