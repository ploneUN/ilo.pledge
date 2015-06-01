from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge import IPledge

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPledge)
    grok.require('zope2.View')
    grok.template('pledge_view')
    grok.name('view')

