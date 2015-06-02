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

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from ilo.pledge import MessageFactory as _


# Interface class; used to define content-type schema.

class InvalidEmailAddress(ValidationError):
    "Invalid email address"


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

    pledges = schema.TextLine(
           title=_(u"Pledges"),
           required=False,
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
