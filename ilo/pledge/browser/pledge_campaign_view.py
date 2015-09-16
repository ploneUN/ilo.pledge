from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge_detail import IPledgeDetail
from ilo.socialsticker.content.sticker import ISticker
from ilo.pledge.content.pledge import IPledge
from ilo.pledge.content.selfie import ISelfie

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
        brains = catalog.unrestrictedSearchResults(object_provides=ISelfie.__identifier__, review_state='published', sort_on='Date',sort_order='reverse')
        return brains
    
    def map_contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__,review_state='published')
    	return brains
    
    def map_count(self):
        results = {}
        pledges = self.map_contents()
        for pledge in pledges:
            obj = pledge._unrestrictedGetObject()
            if obj.country:
                country = self.correct_country_map(obj.country.lower())
                if country not in results:
                    results[country] = 1
                else:
                    results[country] += 1
        
        return results
    
    def correct_country_map(self, country):
        countries = {'bolivia (plurinational state of)':'plurinational state of bolivia',
                     'congo democratic republic of the ':'democratic republic of the congo',
                     'iran islamic republic of': 'islamic republic of iran',
                     'korea democratic peoples republic of': 'democratic peoples republic of korea',
                     'korea republic of': 'republic of korea',
                     'macedonia republic of': 'republic of macedonia',
                     'tanzania united republic of': 'united republic of tanzania',
                     'venezuela (bolivarian republic of)': 'bolivarian republic of venezuela'}
        if country in countries:
            return countries[country]
        return country
        
        
    

