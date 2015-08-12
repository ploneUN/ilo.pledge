
from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.selfie import ISelfie
from ilo.pledge.content.pledge_detail import IPledgeDetail
from ilo.socialsticker.content.sticker import ISticker
from ilo.pledge.content.pledge import IPledge
from plone import api


grok.templatedir('templates')

class pendingstatus_view(dexterity.DisplayForm):
    grok.context(IPledgeCampaign)
    grok.require('zope2.View')
    grok.template('pendingstatus_view')

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def pendingselfie(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(object_provides=ISelfie.__identifier__,review_state= ['private','pending'], sort_on='Date',sort_order='reverse')
        return brains


    def pendingpledge(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        # brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledge',review_state='published')
        brains = catalog.unrestrictedSearchResults(object_provides=IPledge.__identifier__, review_state= ['private','pending'])
        results = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            results.append({'firstname': obj.first_name,
                            'lastname': obj.last_name,
                            'country': obj.country,
                            'path':brain.getPath()})
        return sorted(results, key=lambda data: data['firstname'].lower()) 


    def pledge_detail(self, uid = None):
        catalog = self.catalog
        context = self.context
        result = ""
        brains = catalog.unrestrictedSearchResults(object_provides=IPledgeDetail.__identifier__, UID= uid)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            result = obj.pledge_detail
        return result

    def roles(self):
        current = api.user.get_current()
        roles = api.user.get_roles(username=str(current))
        return any((True for x in roles if x in ['Reviewer', 'Administrator', 'Manager'] ))



