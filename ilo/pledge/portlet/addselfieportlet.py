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
    
    selfie_title = schema.TextLine(
            title = u"Seflie Portlet Title",
            required=False,
        )

    selfie_body = schema.Text(
            title = u"Selfie Portlet Body",
            required=False,
        )

    selfie_description = schema.TextLine(
            title = u"Add Selfie Button Label",
            required=False,
        )


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, selfie_description=None, selfie_title=None, selfie_body= None):
        self.selfie_description = selfie_description
        self.selfie_title = selfie_title
        self.selfie_body = selfie_body
       
    @property
    def title(self):
        return "Add Selfie"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/addselfieportlet.pt')
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
    label = u"Add Selfie Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Edit Selfie Portlet"
    description = ''
