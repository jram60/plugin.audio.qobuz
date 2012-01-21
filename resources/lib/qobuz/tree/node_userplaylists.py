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

import pprint

import qobuz
from constants import *
from flag import NodeFlag
from node import node
from debug import info
'''
    NODE USER PLAYLISTS
'''
from data.userplaylists import QobuzUserPlaylists
from utils.tag import QobuzTagUserPlaylist
from node_playlist import node_playlist

class node_userplaylists(node):
    
    def __init__(self, parent = None):
        super(node_userplaylists, self).__init__(parent)
        self.label  = 'User Playlists'
        self.label2 = 'Keep your current playlist'
        self.type = NodeFlag.TYPE_NODE | NodeFlag.TYPE_USERPLAYLISTS
    
    
    def _build_down(self, lvl, flag = None):
        info(self, "Build Down")
        o = QobuzUserPlaylists(qobuz.api, qobuz.path.cache, -1)
        self.setJson(o.get_data())
        for playlist in self.getJson():
            c = node_playlist()
            c.setId(playlist['id'])
            c.setLabel(playlist['name'])
            c.setJson(playlist)
            self.add_child(c)

    def get_xbmc_item(self, list):
        for c in self.childs:
            c.get_xbmc_item(list)