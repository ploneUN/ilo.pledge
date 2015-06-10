from five import grok
from Acquisition import aq_inner
from plone.app.layout.viewlets.interfaces import IAboveContent
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge_campaign import IPledgeCampaign

grok.templatedir('templates')

class pledgeslink_viewlet(grok.Viewlet):
    grok.context(IPledgeCampaign)
    grok.require('zope2.View')
    grok.template('pledgeslink_viewlet')
    grok.viewletmanager(IAboveContent)

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.aq_parent.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledgecampaign',review_state='published')
        return brains




