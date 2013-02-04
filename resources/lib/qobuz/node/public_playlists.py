'''
    qobuz.node.public_playlists
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This file is part of qobuz-xbmc

    :copyright: (c) 2012 by Joachim Basmaison, Cyril Leclerc
    :license: GPLv3, see LICENSE for more details.
'''
from qobuz.node import Flag, getNode
from inode import INode
from xbmcpy.util import lang, getImage
from qobuz.api import api

class Node_public_playlists(INode):

    def __init__(self, parameters={}):
        super(Node_public_playlists, self).__init__(parameters)
        self.kind = Flag.PUBLIC_PLAYLISTS
        self.label = lang(30008)
        self.image = getImage('userplaylists')
        self.offset = self.get_parameter('offset') or 0

    def fetch(self):
        data = api.get('/playlist/getPublicPlaylists', offset=self.offset, 
                       limit=api.pagination_limit, type='last-created')
        if not data:
            return False
        # @bug: we use pagination_limit as limit for the search so we don't 
        # need offset... (Fixed if qobuz fix it :p)
        if not 'total' in data['playlists']:
            data['playlists']['total'] = data['playlists']['limit']
        self.data = data
        return True

    def populate(self, directory=None, depth=None):
        for item in self.data['playlists']['items']:
            node = getNode(Flag.PLAYLIST, self.parameters)
            node.data = item
            self.append(node)
        return True
