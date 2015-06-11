from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget


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

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer

from ilo.pledge import MessageFactory as _


# Interface class; used to define content-type schema.

class IPledgeDetail(form.Schema, IImageScaleTraversable):
    """
    Pledge Detail
    """

    # form.widget(pledge_detail=WysiwygFieldWidget)
    pledge_detail = schema.Text(title=u"Pledge Detail")
    pledge_logo = NamedBlobFile(
        title=u'Upload Pledge Loge',
        required=True,
    )
    pass

alsoProvides(IPledgeDetail, IFormFieldProvider)

@grok.subscribe(IPledgeDetail, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IPledgeDetail.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    new_id = str(idnormalizer.normalize(context.pledge_detail))
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        new_id = new_id +'-'+str(len(test))
    parent.manage_renameObject(id, new_id )
    context.setTitle('Pledge Detail '+ str(len(object_Ids)))

    context.reindexObject()
    return
