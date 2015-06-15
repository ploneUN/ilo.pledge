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
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from plone.i18n.normalizer import idnormalizer
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent, IAfterTransitionEvent


# Interface class; used to define content-type schema.

class ISelfie(form.Schema, IImageScaleTraversable):
    """
    Selfie
    """
    selfie_owner = schema.TextLine(
           title=_(u"Name"),
           required=True,
        )

    selfie_image = NamedBlobFile(
        title=u'Upload Selfie',
        required=True,
    )

    selfie_message = schema.Text(
           title=_(u"Message"),
           required=True,
        )

    pass

alsoProvides(ISelfie, IFormFieldProvider)




@grok.subscribe(ISelfie, IObjectAddedEvent)
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
    

    selfie_owner = str(idnormalizer.normalize(context.selfie_owner))
    test = ''
    num = 0
    # import pdb; pdb.set_trace()
    if selfie_owner in object_Ids:
        test = filter(lambda name: selfie_owner in name, object_Ids)
        selfie_owner = selfie_owner +'-' + str(len(test))

    parent.manage_renameObject(id, selfie_owner )
    context.setTitle(context.selfie_owner)

    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True

    context.reindexObject()
    return

@grok.subscribe(ISelfie, IAfterTransitionEvent)
def _changeState(context, event):
    wf = getToolByName(context, 'portal_workflow')
    curr_state = wf.getInfoFor(context, 'review_state')
    if curr_state == 'pending':
        context.plone_utils.addPortalMessage(_(u"Your submission will be accepted after review."), "success")
    return

