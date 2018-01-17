from five import grok
from plone.directives import dexterity, form
from ilo.pledge.content.pledge import IPledge
from Products.CMFCore.utils import getToolByName
from ilo.pledge.content.pledge_detail import IPledgeDetail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Products.CMFDefault.utils import checkEmailAddress
import os


grok.templatedir('templates')

def validateaddress(value):
    try:
        checkEmailAddress(value)
        return True
    except Exception:
        return False

class Index(dexterity.DisplayForm):
    grok.context(IPledge)
    grok.require('zope2.View')
    grok.template('pledge_view')
    grok.name('view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 0}, portal_type='ilo.pledge.pledge')
    	return brains

    def pledge_detail(self, uid = None):
        catalog = self.catalog
        context = self.context
        result = ""
        brains = catalog.unrestrictedSearchResults(object_provides=IPledgeDetail.__identifier__, UID= uid)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            result = obj.pledge_detail
        return result
    
    def pledge_logo(self):
        context = self.context
        #path = '/'.join(context.getPhysicalPath())
        path = context.absolute_url()
        if len(context.pledges):
            return path+'/++theme++idwfed.theme/pd_img/pd_img_'+str(len(context.pledges))+'.png'
        return ''

    # def current_url(self):
    #     request = self.request
    #     field = ''
    #     if request.form:
    #         if 'fb_ref' in request.form:
    #             field = request.form['fb_ref']
    #     return field

    def sendEmail(self):
        request = self.request
        context = self.context
        mailhost = getToolByName(context, 'MailHost')
        if request:
            if 'to_email' in request.form:
                form = request.form
                email1 = context.email1
                
                to_email = form['to_email']
                sender_email = form['sender_email']
                def_message = form['message']
                if not validateaddress(to_email):
                    context.plone_utils.addPortalMessage(u"Please enter valid email address.", 'info')
                    request.RESPONSE.redirect('/'.join(context.getPhysicalPath()))
                    return
                if not validateaddress(sender_email):
                    context.plone_utils.addPortalMessage(u"Please enter valid sender's email address.", 'info')
                    request.RESPONSE.redirect('/'.join(context.getPhysicalPath()))
                    return
                if email1 != sender_email:
                    context.plone_utils.addPortalMessage(u"Please enter valid sender's email address.", 'info')
                    request.RESPONSE.redirect('/'.join(context.getPhysicalPath()))
                else:
                    message = MIMEMultipart('alternative')
                    message['Subject'] = "I pledged to uphold pricinciples of c189"
                    message["From"] = sender_email
                    message['To'] = to_email
                    html = """<html><head></head><body>"""
                    html += """<a src="""+context.absolute_url()+""">"""
                    html += """<img src="""+self.pledge_logo()+""" title="" alt=""/>"""
                    html += """</a>"""
                    html += """<br/>"""
                    if def_message:
                        html += """<p>Message:<br/>"""
                        html += def_message+"""</p>"""
                    html += """Pledge Item:"""
                    if context.pledges:
                        html += """<ul>"""
                        pledges = context.pledges
                        for pledge in pledges:
                            html += """<li>"""+self.pledge_detail(pledge)+"""</li>"""
                        html += """</ul>"""
                    html += """</body></html>"""
                    
                    part1 = MIMEText(html, 'html')
                    message.attach(part1)
                    try:
                        mailhost.send(message)
                        context.plone_utils.addPortalMessage(u'Successfully mailed.', 'success')
                        request.RESPONSE.redirect('/'.join(context.getPhysicalPath()))
                    except ValueError, e:
                        context.plone_utils.addPortalMessage(u'Unable to send email', 'info')
                        request.RESPONSE.redirect('/'.join(context.getPhysicalPath()))
                    
    
    def text_direction_value(self):
        parent = self.context.aq_parent
        value = 'ltr'
        if hasattr(parent, 'text_direction'):
            if parent.text_direction:
                value = parent.text_direction
        return value