from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledges import IPledges

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPledges)
    grok.require('zope2.View')
    grok.template('pledges_view')
    grok.name('view')

