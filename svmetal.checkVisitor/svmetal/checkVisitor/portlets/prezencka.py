#-*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from svmetal.checkVisitor import checkVisitorMessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

import datetime

class User():
    login = ""
    date = ""
    
    def __init__(self, login):
        self.login = login
        self.date = datetime.date.today()

class Iprezencka(IPortletDataProvider):
    header = schema.TextLine(title=_(u'Název'),
                             default=u"",
                             description=_(u'Název portletu'),
                             required=False)
    
    date = schema.Bool(title=_(u'Datum poslední návštěvy'),
                       description=_(u'Zobrazovat datum poslední návštěvy uživatele'),
                       default=False,
                       required=False)
    

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(Iprezencka)
    users = []
    
    def __init__(self, header="Prezenčka", date=False):
        self.header = header
        self.date = date
        self.users = []

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(self.header)
    
    @property
    def visitDate(self):
        return self.date
    
    @property
    def us(self):
        return self.users

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    def setUser(self):
        context = self.context.aq_inner
        ms = getToolByName(self.context, 'portal_membership')
        member = ms.getAuthenticatedMember()
        us = member.getUserName()
        visit = False
        for user in self.data.users:
            if us == user.login:
                visit = True
                user.date = datetime.date.today()
                break
        if not visit:
            self.data.users.append(User(us))
        
    
    render = ViewPageTemplateFile('prezencka.pt')


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(Iprezencka)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(Iprezencka)
