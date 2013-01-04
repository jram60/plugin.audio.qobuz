#     Copyright 2011 Joachim Basmaison, Cyril Leclerc
#
#     This file is part of xbmc-qobuz.
#
#     xbmc-qobuz is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     xbmc-qobuz is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with xbmc-qobuz.   If not, see <http://www.gnu.org/licenses/>.
import xbmcgui
import xbmc

import qobuz
from flag import NodeFlag as Flag
from inode import INode
from recommendation import Node_recommendation, RECOS_TYPE_IDS
from gui.util import getImage

'''
    @class Node_genre:
'''

class Node_genre(INode):

    def __init__(self, parent=None, parameters=None, progress=None):
        super(Node_genre, self).__init__(parent, parameters)
        self.type = Flag.GENRE
        self.set_label('Genre (i8n)')
        self.is_folder = True
        self.image = getImage('album')

    def make_url(self, **ka):
        url = super(Node_genre, self).make_url(**ka)
        if self.parent and self.parent.id:
            url += "&parent-id=" + self.parent.id
        return url

    def hook_post_data(self):
        self.id = self.get_property('id')
        self.label = self.get_property('name')

    def get_name(self):
        return self.get_property('name')

    def _build_down_reco(self, directory, lvl, whiteFlag, blackFlag, ID):
        for gtype in RECOS_TYPE_IDS:
            print "Build Node RECO %s / %s" % (ID, gtype)
            node = Node_recommendation(
                self, {'genre-id': ID, 'genre-type': gtype})
            node.build_down(directory, -1, Flag.PRODUCT, blackFlag)
        return True

    def pre_build_down(self, Dir, lvl , whiteFlag, blackFlag):
        offset = self.get_parameter('offset') or 0
        limit = qobuz.addon.getSetting('pagination_limit')
        data = qobuz.registry.get(
            name='genre-list', id=self.id, offset=offset, limit=limit)
        if not data: 
            self.data = None
            return True
        self.data = data['data']
        return True

    def _build_down(self, directory, lvl, whiteFlag, blackFlag):
        if not self.data or len(self.data['genres']['items']) == 0:
            return self._build_down_reco(directory, lvl, 
                                         whiteFlag, blackFlag, self.id)
        for genre in self.data['genres']['items']:
            node = Node_genre(self, {'nid': self.id})
            node.data = genre
            if 'parent' in genre and genre['parent']['level'] > 1:
                self._build_down_reco(directory, lvl, whiteFlag, genre['id'])
            self.add_child(node)
        return True
