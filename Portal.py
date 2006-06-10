import os

from Products.CMFDefault.Portal import CMFSite

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFDefault import DublinCore
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.PloneFolder import OrderedContainer
import Globals

from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from Acquisition import aq_base
from ComputedAttribute import ComputedAttribute
from webdav.NullResource import NullResource
from Products.CMFPlone.PloneFolder import ReplaceableWrapper
from Products.CMFPlone.utils import log_exc
from Products.CMFPlone.utils import WWW_DIR
from Products.CMFPlone.interfaces import IPloneSiteRoot

from zope.interface import implements

member_indexhtml="""\
member_search=context.restrictedTraverse('member_search_form')
return member_search()
"""

class PloneSite(CMFSite, OrderedContainer, BrowserDefaultMixin):
    """
    Make PloneSite subclass CMFSite and add some methods.
    This will be useful for adding more things later on.
    """
    security=ClassSecurityInfo()
    meta_type = portal_type = 'Plone Site'

    implements(IPloneSiteRoot)

    __implements__ = DublinCore.DefaultDublinCoreImpl.__implements__ + \
                     OrderedContainer.__implements__ + \
                     BrowserDefaultMixin.__implements__

    manage_renameObject = OrderedContainer.manage_renameObject

    moveObject = OrderedContainer.moveObject
    moveObjectsByDelta = OrderedContainer.moveObjectsByDelta

    # Switch off ZMI ordering interface as it assumes a slightly
    # different functionality
    has_order_support = 0
    manage_main = Globals.DTMLFile('www/main', globals())

    def __browser_default__(self, request):
        """ Set default so we can return whatever we want instead
        of index_html """
        return getToolByName(self, 'plone_utils').browserDefault(self)

    def index_html(self):
        """ Acquire if not present. """
        request = getattr(self, 'REQUEST', None)
        if request and request.has_key('REQUEST_METHOD'):
            if request.maybe_webdav_client:
                method = request['REQUEST_METHOD']
                if method in ('PUT',):
                    # Very likely a WebDAV client trying to create something
                    return ReplaceableWrapper(NullResource(self, 'index_html'))
                elif method in ('GET', 'HEAD', 'POST'):
                    # Do nothing, let it go and acquire.
                    pass
                else:
                    raise AttributeError, 'index_html'
        # Acquire from skin.
        _target = self.__getattr__('index_html')
        return ReplaceableWrapper(aq_base(_target).__of__(self))

    index_html = ComputedAttribute(index_html, 1)

    def manage_beforeDelete(self, container, item):
        """ Should send out an Event before Site is being deleted """
        self.removal_inprogress=1
        PloneSite.inheritedAttribute('manage_beforeDelete')(self, container, item)

    def _management_page_charset(self):
        """ Returns default_charset for management screens """
        properties = getToolByName(self, 'portal_properties', None)
        # Let's be a bit careful here because we don't want to break the ZMI
        # just because people screw up their Plone sites (however thoroughly).
        if properties is not None:
            site_properties = getattr(properties, 'site_properties', None)
            if site_properties is not None:
                getProperty = getattr(site_properties, 'getProperty', None)
                if getProperty is not None:
                    return getProperty('default_charset', 'utf-8')
        return 'utf-8'

    management_page_charset = ComputedAttribute(_management_page_charset, 1)

    def view(self):
        """ Ensure that we get a plain view of the object, via a delegation to
        __call__(), which is defined in BrowserDefaultMixin
        """
        return self()

    security.declareProtected(permissions.AccessContentsInformation,
                 'folderlistingFolderContents')
    def folderlistingFolderContents(self, spec=None, contentFilter=None):
        """Calls listFolderContents in protected only by ACI so that
        folder_listing can work without the List folder contents permission,
        as in CMFDefault.

        This is copied from Archetypes Basefolder and is needed by the
        reference browser.
        """
        return self.listFolderContents(spec, contentFilter)

    security.declareProtected(permissions.DeleteObjects,
                              'manage_delObjects')
    def manage_delObjects(self, ids=[], REQUEST=None):
        """We need to enforce security."""
        mt = getToolByName(self, 'portal_membership')
        if type(ids) is str:
            ids = [ids]
        for id in ids:
            item = self._getOb(id)
            if not mt.checkPermission(permissions.DeleteObjects, item):
                raise Unauthorized, (
                    "Do not have permissions to remove this object")
        return CMFSite.manage_delObjects(self, ids, REQUEST=REQUEST)

Globals.InitializeClass(PloneSite)
