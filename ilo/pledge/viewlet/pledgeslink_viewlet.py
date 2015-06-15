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
    
    def hideAllPledgesLink(self, ):
        url = self.request.URL
        if '++add++' in url:
            return False
        return True
    


