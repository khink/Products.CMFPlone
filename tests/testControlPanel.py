#
# Tests the ControlPanel
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFPlone.tests import PloneTestCase


class TestControlPanel(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.controlpanel = self.portal.portal_controlpanel
        # get the expected default groups and configlets
        self.groups     = ['Plone', 'Products', 'Member']
        self.configlets = ['Add/Remove Products', 'Smart Folder Settings',
                           'Users and Groups Administration', 'Mail Settings',
                           'Personal Preferences', 'Change Password', 'Skins',
                           'Zope Management Interface', 'Navigation Settings',
                           'Placeful Workflow', 'Search Settings', 'Error Log',
                           'Kupu visual editor', 'Portal Settings']

    def testDefaultGroups(self):
        for group in self.groups:
            self.failUnless(group in self.controlpanel.getGroupIds(),
                            "Missing group with id '%s'" % group)

    def testDefaultConfiglets(self):
        for title in self.configlets:
            self.failUnless(title in [a.getAction(self)['title']
                                   for a in self.controlpanel.listActions()],
                            "Missing configlet with title '%s'" % title)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestControlPanel))
    return suite

if __name__ == '__main__':
    framework()