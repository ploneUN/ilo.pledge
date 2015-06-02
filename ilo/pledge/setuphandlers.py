from collective.grok import gs
from ilo.pledge import MessageFactory as _

from Products.CMFPlone.utils import _createObjectByType
from collective.setuphelpers.structure import clearUpSite, setupStructure

@gs.importstep(
    name=u'ilo.pledge', 
    title=_('ilo.pledge import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ilo.pledge.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
