from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.selfie import ISelfie

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ISelfie)
    grok.require('zope2.View')
    grok.template('selfie_view')
    grok.name('view')

