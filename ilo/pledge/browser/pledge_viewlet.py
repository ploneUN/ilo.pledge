from five import grok
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge import IPledge
from plone.app.layout.viewlets.interfaces import IAboveContent

grok.templatedir('templates')

class pledge_viewlet(grok.Viewlet):
    grok.context(IPledge)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)