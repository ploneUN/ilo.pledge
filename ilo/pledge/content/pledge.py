from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from quintagroup.z3cform.captcha import Captcha, CaptchaWidgetFactory
from collective import dexteritytextindexer

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.i18n.normalizer import idnormalizer

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from ilo.pledge import MessageFactory as _
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.i18n.normalizer import idnormalizer
from ilo.pledge.content.pledge_detail import IPledgeDetail
# Interface class; used to define content-type schema.

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

#pledge detail vocabulary for dropdown
@grok.provider(IContextSourceBinder)
def pledge_details(context):
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IPledgeDetail.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
    results = []
    for brain in brains:
        results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=brain.Title))
    return SimpleVocabulary(results)

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class IPledge(form.Schema, IImageScaleTraversable):
    """
    Pledge Form
    """
    first_name = schema.TextLine(
           title=_(u"First Name"),
           required=True,
        )

    last_name = schema.TextLine(
           title=_(u"Last Name"),
           required=True,
        )

    middle_initial = schema.TextLine(
           title=_(u"Middle Initial"),
           required=True,
        )

    city = schema.TextLine(
            title=_(u"City"),
            required=False,
         )

    country = schema.TextLine(
           title=_(u"Country"),
           required=False,
        )

#this should be the id of the pledge
    email1 = schema.TextLine(
           title=_(u"Email Address"),
           constraint=validateaddress,
        )

    email2 = schema.TextLine(
           title=_(u"Enter the same email address"),
           constraint=validateaddress
        )

    # pledges = schema.TextLine(
    #        title=_(u"Pledges"),
    #        required=False,
    #     )

    pledges = schema.Choice(
            title = _(u"Pledges"),
            required = False,
            source = pledge_details,
        )

    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
    
    @invariant
    def emailAddressValidation(self):
        #pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            
        if self.email1 != self.email2:
            raise Invalid(_("Both email addresses do not match"))
        
        #if not bool(re.match(pattern, self.email1)):
        #    raise Invalid(_(u"Email 1 is not a valid email address."))
        #elif not bool(re.match(pattern, self.email2  )):
        #    raise Invalid(_(u"Email 2 is not a valid email address."))


    pass

alsoProvides(IPledge, IFormFieldProvider)


@grok.subscribe(IPledge, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = str(idnormalizer.normalize(context.last_name))
    first_name = str(idnormalizer.normalize(context.first_name))
    temp_new_id = last_name+'_'+first_name
    new_id = temp_new_id.replace("-","")
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[-1])+1) 

    parent.manage_renameObject(id, new_id )
    context.setTitle(context.email1)

    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True

    context.reindexObject()
    return