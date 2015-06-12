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
from collective import dexteritytextindexer

from ilo.pledge import MessageFactory as _


# Interface class; used to define content-type schema.

class INetworking(form.Schema, IImageScaleTraversable):
    """
    Networking
    """

    full_name = schema.TextLine(
           title=_(u"Name"),
           required=True,
        )

    email = schema.TextLine(
           title=_(u"Email"),
           required=True,
        )

    location = schema.TextLine(
           title=_(u"Location"),
           required=True,
        )

    interested = schema.Bool(
        title=u'Click here if you are interested in learning more about domestic workers’ rights in your region.',
        required=False,
        default=False
    )

    pass

alsoProvides(INetworking, IFormFieldProvider)

@grok.subscribe(INetworking, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    # brains = catalog.unrestrictedSearchResults(object_provides = ISelfie.__identifier__)

    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1})
    for brain in brains:
        object_Ids.append(brain.id)
    

    full_name = str(idnormalizer.normalize(context.selfie_owner))
    test = ''
    num = 0
    if full_name in object_Ids:
        test = filter(lambda name: full_name in name, object_Ids)
        full_name = full_name +'-' + str(len(test))

    parent.manage_renameObject(id, selfie_owner )
    context.setTitle(context.full_name)

    context.reindexObject()
    return
