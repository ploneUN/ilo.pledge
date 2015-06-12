from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.networking import INetworking

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(INetworking)
    grok.require('zope2.View')
    grok.template('networking_view')
    grok.name('view')

