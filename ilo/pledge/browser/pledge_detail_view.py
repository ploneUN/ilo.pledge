from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_detail import IPledgeDetail

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPledgeDetail)
    grok.require('zope2.View')
    grok.template('pledge_detail_view')
    grok.name('view')

