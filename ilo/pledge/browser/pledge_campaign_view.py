from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge_detail import IPledgeDetail
from ilo.socialsticker.content.sticker import ISticker

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPledgeCampaign)
    grok.require('zope2.View')
    grok.template('pledge_campaign_view')
    grok.name('view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledge',review_state='published')
    	return brains

    def pledge_detail(self, uid = None):
        catalog = self.catalog
        context = self.context
        result = ""
        brains = catalog.unrestrictedSearchResults(object_provides=IPledgeDetail.__identifier__, UID= uid)
        for brain in brains:
            result = brain.Title
        return result

    def sticker(self, uid = None):
        catalog = self.catalog
        context = self.context
        result = ""
        brains = catalog.unrestrictedSearchResults(object_provides=ISticker.__identifier__, UID= uid)
        for brain in brains:
            result = brain.getPath()
        return result

    def pledge_details(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth': 1}, portal_type='ilo.pledge.pledgedetail', review_state='published')
        return brains

    def selfies(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth': 1}, portal_type='ilo.pledge.selfie', review_state='published', sort_on='Date',sort_order='reverse')[:13]
        return brains
    
    def map_count(self):
        results = {}
        pledges = self.contents()
        for pledge in pledges:
            obj = pledge._unrestrictedGetObject()
            if obj.country:
                country = obj.country.lower()
                if country not in results:
                    results[country] = 1
                else:
                    results[country] += 1
        
        return results
        
        
    

