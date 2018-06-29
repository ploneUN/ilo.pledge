from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge_campaign import IPledgeCampaign
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge_detail import IPledgeDetail
from ilo.socialsticker.content.sticker import ISticker
from ilo.pledge.content.pledge import IPledge

grok.templatedir('templates')

class pledges_view(dexterity.DisplayForm):
    grok.context(IPledgeCampaign)
    grok.require('zope2.View')
    grok.template('pledges_view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledge',review_state='published')
        #brains = catalog.unrestrictedSearchResults(object_provides=IPledge.__identifier__, review_state='published')
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
    
    def text_direction_value(self):
        value = 'ltr'
        if hasattr(self.context, 'text_direction'):
            if self.context.text_direction:
                value = self.context.text_direction
        return value
    
    def header_css(self):
        return """
                <style ="text/css">
                    h1.documentFirstHeading{
                        direction: %s;
                    }
                </style>
        """ % (self.text_direction_value())

    def number_per_column(self):
        contents = self.contents()
        return int(len(contents)/3) + (len(contents) % 3 > 0)



