from collective.grok import gs
from ilo.pledge import MessageFactory as _

@gs.importstep(
    name=u'ilo.pledge', 
    title=_('ilo.pledge import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ilo.pledge.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
