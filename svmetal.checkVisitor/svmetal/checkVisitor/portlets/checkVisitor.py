#-*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from zope.i18n import MessageFactory
from zope import schema

PMF = MessageFactory('plone')

class ICheckVisitorPortlet(IPortletDataProvider):
    header = schema.TextLine(title=_(u'Název'),
                             default=u"",
                             description=_(u'Název portletu'),
                             required=False)
    

from plone.app.portlets.portlets import base
from zope.interface import implements
class Assignment(base.Assignment):
    implements(ICheckVisitorPortlet)
    
    def __init__(self, header=""):
        self.header = header
        
    @property
    def title(self):
        return PMF(self.header)
    
from zope.formlib import form

class AddForm(base.AddForm):
    form_fields = form.Fields(ICheckVisitorPortlet)
    label = _(u'Portlet ke sledování návštěvníků')
    description = _(u'Přidat portlet na sledování návštěvníků')
    
    def create(self, data):
        return Assignment(**data)
    
class EditForm(base.EditForm):
    form_fields = form.Fields(ICheckVisitorPortlet)
    label = _(u'Edit portlet')
    description = _(u'Upravit portlet na sledování návštěvníků')
    
    
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('checkVisitorView.pt')
    
    def render(self):
        context = self.context
        return self._template()
    
    