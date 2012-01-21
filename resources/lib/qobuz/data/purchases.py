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
import sys
import os
import xbmcgui
import xbmcplugin

import pprint

from debug import *
from constants import *
from utils.icacheable import ICacheable
from tag.track import TagTrack
from tag.album import TagAlbum
import qobuz
"""
    Class QobuzGetPurchases
"""
class QobuzGetPurchases(ICacheable):

    def __init__(self, limit = 100):
        self.limit = limit
        super(QobuzGetPurchases, self).__init__(qobuz.path.cache, 
                                       'purchases')
        self.set_cache_refresh(qobuz.addon.getSetting('cache_duration_recommandation'))
        debug(self, "Cache duration: " + str(self.cache_refresh))
        self.fetch_data()
        
    def _fetch_data(self):
        return qobuz.api.get_purchases(self.limit)
    
    def length(self):
        if not self._raw_data:
            return 0
        return len(self._raw_data)

    def get_items(self):
        list = []
        data = self.get_data()
        if not data:
            return list
        n = self.length()
        albumseen = {}
        needsave = False
        # Qobuz free tracks with invalid product id
        blackid = ['0000020110926', '0000201011300']
        for track in self._raw_data:
            t = TagTrack(track)
            album = t.get_childs_with_type(type(TagAlbum))
            if not album:
                    warn(self, "No album for this track")
                    continue
            album = album[0]
            if album.id in blackid:
                continue
            if album.id in albumseen:
                continue
            item = album.getXbmcItem('fanArt')
            item.setInfo('music', infoLabels = { 'artist': t.getArtist(), 'year': t.getYear()})
            u = qobuz.boot.build_url(MODE_ALBUM, album.id)
            list.append((u, item, True))        
            albumseen[album.id] = 'true'
        return list
