from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget


#grok.templatedir('templates')

class IContentNavigation(IPortletDataProvider):
    
    pledges_description = schema.TextLine(
            title = u"All Pledges Label",
            required=False,
        )

    # pledges_link = schema.TextLine(
    #         title = u"All Pledges Link",
    #         required=False,
    #     )

    selfie_description = schema.TextLine(
            title = u"All Selfie Label",
            required=False,
        )

    # selfie_link= schema.TextLine(
    #         title = u"Selfie Link",
    #         required=False,
    #     )

class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self,pledges_description=None, selfie_description=None):
        self.pledges_description = pledges_description
        # self.pledges_link = pledges_link
        self.selfie_description = selfie_description
        # self.selfie_link = selfie_link
       
    @property
    def title(self):
        return "My Fair Home"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/allpledgesportlet.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
        
    def contents(self):
        return self.data

class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add My Fair Home Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Edit My Fair Home Portlet"
    description = ''
