from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.selfie import ISelfie


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
    	brains = catalog.unrestrictedSearchResults(object_provides=ISelfie.__identifier__,review_state='published', sort_on='Date',sort_order='reverse')
    	return brains

    def pab_commitment_header(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 0})
        result = ''
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            result = obj.pab_commitment_header

        return result




