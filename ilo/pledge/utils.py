from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import json

class ApiView(BrowserView):

    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

class PledgeLogoImage(ApiView):
    
    def __call__(self):
        if self.request:
            if self.request.form:
                form = self.request.form
                path = form['path']
                count = form['count']
                img_src = ''
                if count:
                    img_src = path+'/++theme++idwfed.theme/pd_img/pd_img_'+str(count)+'.png'
        return self._response(response={'img_src':img_src})