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
# from ilo.socialsticker.content.sticker import ISticker
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.DCWorkflow.interfaces import IBeforeTransitionEvent, IAfterTransitionEvent
from z3c.form import validator
# Interface class; used to define content-type schema.

class InvalidEmailAddress(ValidationError):
    "Invalid email address"


# class stickers(object):
#     grok.implements(IContextSourceBinder)
#     def __call__(self,context ):
#         catalog = getToolByName(context, 'portal_catalog')
#         brains = catalog.unrestrictedSearchResults(object_provides = ISticker.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
#         results = []
#         for brain in brains:
#             obj = brain._unrestrictedGetObject()
#             results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=brain.getPath()))
#         return SimpleVocabulary(results)

#pledge detail vocabulary for dropdown
class pledge_details(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context, 'portal_catalog')
        #brains = catalog.unrestrictedSearchResults(object_provides = IPledgeDetail.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
        if context.portal_type == 'ilo.pledge.pledgecampaign':
            path = '/'.join(context.getPhysicalPath())
        else:
            path = '/'.join(context.aq_parent.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledgedetail',review_state='published')
        results = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=obj.pledge_detail))
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
    form.widget(pledges=CheckBoxFieldWidget)
    pledges = schema.List(
        title=u'I commit to uphold the standards of Convention No. 189, and to protect and promote the rights of domestic workers in my home and community, by taking the following actions:',
        required=False,
        value_type=schema.Choice(source=pledge_details())
    )
    
    first_name = schema.TextLine(
           title=_(u"First Name"),
           required=True,
        )

    last_name = schema.TextLine(
           title=_(u"Last Name"),
           required=True,
        )

#    middle_initial = schema.TextLine(
#           title=_(u"Middle Initial"),
#           required=True,
#        )

#    city = schema.TextLine(
#            title=_(u"City"),
#            required=False,
#         )

    country = schema.TextLine(
           title=_(u"Country"),
           required=False,
        )

#    domestic_workers = schema.Bool(
#        title=u'Employer of domestic worker/s',
#        required=False,
#        default=False
#    )

#this should be the id of the pledge
    email1 = schema.TextLine(
           title=_(u"Email Address"),
           constraint=validateaddress,
        )

    email2 = schema.TextLine(
           title=_(u"Verify Email Address"),
           constraint=validateaddress
        )

    
    # form.widget(stickers=CheckBoxFieldWidget)
    # stickers = schema.List(
    #     title=u'Stickers',
    #     required=True,
    #     value_type=schema.Choice(source=stickers())
    # )

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

class CheckDuplicateEmail(validator.SimpleFieldValidator):
    def validate(self, value):
        super(CheckDuplicateEmail, self).validate(value)
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        if context.portal_type == 'ilo.pledge.pledgecampaign':
            brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__)
            emails = [brain._unrestrictedGetObject().email1 for brain in brains]
            if value in emails:
                raise Invalid(_("Email already exists."))
        elif context.portal_type == 'ilo.pledge.pledge':
            brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__)
            emails = [brain._unrestrictedGetObject().email1 for brain in brains if brain.UID != self.context.UID()]
            if value in emails:
                raise Invalid(_("Email already exists."))
            

validator.WidgetValidatorDiscriminators(CheckDuplicateEmail, field=IPledge['email1'])
grok.global_adapter(CheckDuplicateEmail)


@grok.subscribe(IPledge, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1})
    for brain in brains:
        object_Ids.append(brain.id)
    
    email1 = str(idnormalizer.normalize(context.email1))
    new_id = email1.replace('-','_')
    
    test = ''
    num = 0
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        new_id = new_id +'_' + str(len(test))

    parent.manage_renameObject(id, new_id )
    context.setTitle(new_id)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return


@grok.subscribe(IPledge, IObjectModifiedEvent)
def modifyobject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1})
    for brain in brains:
        object_Ids.append(brain.id)
    
    email1 = str(idnormalizer.normalize(context.email1))
    new_id = email1.replace('-','_')
    
    test = ''
    num = 0
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        new_id = new_id +'_' + str(len(test))

    parent.manage_renameObject(id, new_id )
    context.setTitle(new_id)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return

@grok.subscribe(IPledge, IAfterTransitionEvent)
def _changeState(context, event):
    wf = getToolByName(context, 'portal_workflow')
    curr_state = wf.getInfoFor(context, 'review_state')
    mailhost = getToolByName(context, 'MailHost')
    if curr_state == 'pending':
        context.plone_utils.addPortalMessage(_(u"Congratulations on taking the pledge."), "success")
        if context.email1:
            ## Email to afterfive
            mSubj = "Signature Received"
            mFrom = "afterfive2015@gmail.com"
            mTo = "afterfive2015@gmail.com"
            mBody = "A site visitor has just signed the c189 Pledge. Below are the details of the new signatory.\n"
            mBody += "Name: "+context.first_name+" "+context.last_name+"\n"
            #mBody += "City: "+context.city+"\n"
            mBody += "Country: "+context.country+"\n"
            mBody += "Email: "+context.email1+"\n"
            mBody += "\n"
            mBody += "To review the above signature, visit:\n\n"
            mBody += context.absolute_url()+"\n\n"
            mBody += "To approve the post, click on the link below:\n\n"
            mBody += context.absolute_url()+"/content_status_modify?workflow_action=publish"
            mBody += "\n\n"
            
            mBody += "-------------------------\n"
            mBody += "IDWF Portal"
            
            
            mSubj_1 = "Pledge Received"
            mTo_1 = context.email1
            mBody_1 = "This is to confirm that you have signed the c189 Pledge.  You may view your signature details from the link below:\n\n"
            mBody_1 += context.absolute_url()+"\n\n"
            mBody_1 += "We will review your submission and once approved, your name will appear in the list of supporters.\n\n"
            mBody_1 += "If you find that there are errors to your submission, please email afterfive2015@gmail.com\n\n"
            mBody_1 += "If you would like us to keep you up-to-date with the latest information, please sign up for our newsletter at www.idwf.org\n\n"
            mBody_1 += "\n\n\n"
            mBody_1 += "-------------------------\n"
            mBody_1 += "IDWF Portal\n"
            mBody_1 += "http://www.idwf.org"
            
            try:
                mailhost.send(mBody, mto=mTo, mfrom=mFrom, subject=mSubj, immediate=True, charset='utf8', msg_type=None)
                
                mailhost.send(mBody_1, mto=mTo_1, mfrom=mFrom, subject=mSubj_1, immediate=True, charset='utf8', msg_type=None)
            except ValueError, e:
                context.plone_utils.addPortalMessage(u'Unable to send email', 'info')
                return None


class PledgeAddForm(dexterity.AddForm):
    grok.name('ilo.pledge.pledge')
    template = ViewPageTemplateFile('templates/pledgeaddform.pt')
    form.wrap(False)
    

class PledgeEditForm(dexterity.EditForm):
    grok.context(IPledge)
    template = ViewPageTemplateFile('templates/pledgeeditform.pt')


