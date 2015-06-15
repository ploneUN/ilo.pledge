from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName


grok.templatedir('templates')

class selfies_view(dexterity.DisplayForm):
    grok.context(IPledgeCampaign)
    grok.require('zope2.View')
    grok.template('selfies_view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.selfie',review_state='published', sort_on='Date',sort_order='reverse')
    	return brains




