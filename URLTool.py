from Products.CMFCore.URLTool import URLTool as BaseTool
from Products.CMFPlone import ToolNames
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

class URLTool(BaseTool):

    meta_type = ToolNames.URLTool
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/link_icon.gif'

URLTool.__doc__ = BaseTool.__doc__

InitializeClass(URLTool)
