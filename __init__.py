# Copyright (c) 2007-2010 Infrae. All rights reserved.
# See also LICENSES.txt
# $Id$

from zope.interface import Interface
from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller, roleinfo

silvaconf.extensionName('SilvaForum')
silvaconf.extensionTitle('Silva Forum')


class IExtension(Interface):
    """Silva Forum extension.
    """


class SilvaForumInstaller(DefaultInstaller):
    not_globally_addables = ['Silva Forum Topic', 'Silva Forum Comment']
    default_permissions = {'Silva Forum': roleinfo.EDITOR_ROLES}
    metadata = {('Silva Forum Topic', 'Silva Forum Comment'):
                    ('silva-content', 'silva-extra', 'silvaforum-item'),
                ('Silva Forum',):
                    ('silva-content', 'silva-extra', 'silva-layout'),
                ('Silva Forum', 'Silva Forum Topic'):
                    ('silvaforum-forum',)}

    def install_custom(self, root):
        self.configure_metadata(root, self.metadata, globals())

    def uninstall_custom(self, root):
        self.unconfigure_metadata(root, self.metadata)


install = SilvaForumInstaller('SilvaForum', IExtension)
