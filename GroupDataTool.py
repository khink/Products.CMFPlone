from Products.GroupUserFolder.GroupDataTool import GroupDataTool as BaseTool

from Products.CMFPlone import ToolNames
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

class GroupDataTool(BaseTool):

    meta_type = ToolNames.GroupDataTool
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/group.gif'

GroupDataTool.__doc__ = BaseTool.__doc__

InitializeClass(GroupDataTool)
